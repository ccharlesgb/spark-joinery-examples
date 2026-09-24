from collections.abc import Generator
from datetime import UTC, datetime

import pytest
from order_product.context import CustomersPath, OrdersPath, OutputPath, RunDate
from order_product.schemas import Customer, Order, OrderWithCustomerDimension
from order_product.transform import (
    filter_orders,
    join_orders_with_customers,
    read_customers,
    read_orders,
    write_output,
)
from pyspark.sql import SparkSession
from pyspark.testing import assertDataFrameEqual
from spark_joinery import Schema


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession]:
    session = (
        SparkSession.builder.master("local[1]")
        .appName("order-product-transform-tests")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_read_orders_reads_parquet_rows(spark: SparkSession, tmp_path):
    # Given
    input_orders = Schema(Order).create_dataframe(
        spark,
        [Order(1, "customer-1", datetime(2026, 9, 24, 8, 30, tzinfo=UTC), 100, 2)],
    )
    expected_orders = Schema(Order).create_dataframe(
        spark,
        [Order(1, "customer-1", datetime(2026, 9, 24, 8, 30, tzinfo=UTC), 100, 2)],
    )
    path = tmp_path / "orders"
    input_orders.write.parquet(str(path))

    # When
    actual = read_orders(spark, OrdersPath(str(path)))

    # Then
    assertDataFrameEqual(actual, expected_orders)


def test_filter_orders_keeps_only_orders_for_run_date(spark: SparkSession):
    # Given
    input_orders = Schema(Order).create_dataframe(
        spark,
        [
            Order(1, "customer-1", datetime(2026, 9, 24, 8, 30, tzinfo=UTC), 100, 2),
            Order(2, "customer-2", datetime(2026, 9, 25, 9, 45, tzinfo=UTC), 200, 1),
        ],
    )
    expected_orders = Schema(Order).create_dataframe(
        spark,
        [Order(1, "customer-1", datetime(2026, 9, 24, 8, 30, tzinfo=UTC), 100, 2)],
    )

    # When
    actual = filter_orders(input_orders, RunDate(2026, 9, 24))

    # Then
    assertDataFrameEqual(actual, expected_orders)


def test_read_customers_reads_parquet_rows(spark: SparkSession, tmp_path):
    # Given
    input_customers = Schema(Customer).create_dataframe(
        spark,
        [Customer("customer-1", "Ada")],
    )
    expected_customers = Schema(Customer).create_dataframe(
        spark,
        [Customer("customer-1", "Ada")],
    )
    path = tmp_path / "customers"
    input_customers.write.parquet(str(path))

    # When
    actual = read_customers(spark, CustomersPath(str(path)))

    # Then
    assertDataFrameEqual(actual, expected_customers)


def test_join_orders_with_customers_keeps_matched_orders(spark: SparkSession):
    # Given
    input_orders = Schema(Order).create_dataframe(
        spark,
        [
            Order(1, "customer-1", datetime(2026, 9, 24, 8, 30, tzinfo=UTC), 100, 2),
            Order(2, "customer-2", datetime(2026, 9, 25, 9, 45, tzinfo=UTC), 200, 1),
        ],
    )
    input_customers = Schema(Customer).create_dataframe(
        spark,
        [
            Customer("customer-1", "Ada"),
            Customer("customer-3", "Grace"),
        ],
    )
    expected_orders = Schema(OrderWithCustomerDimension).create_dataframe(
        spark,
        [
            OrderWithCustomerDimension(
                order_id=1,
                customer_id="customer-1",
                order_timestamp=datetime(2026, 9, 24, 8, 30, tzinfo=UTC),
                product_id=100,
                quantity=2,
                name="Ada",
            )
        ],
    )

    # When
    actual = join_orders_with_customers(input_orders, input_customers)

    # Then
    assertDataFrameEqual(actual, expected_orders)


def test_write_output_writes_parquet_rows(spark: SparkSession, tmp_path):
    # Given
    input_orders = Schema(OrderWithCustomerDimension).create_dataframe(
        spark,
        [
            OrderWithCustomerDimension(
                order_id=1,
                customer_id="customer-1",
                order_timestamp=datetime(2026, 9, 24, 8, 30, tzinfo=UTC),
                product_id=100,
                quantity=2,
                name="Ada",
            )
        ],
    )
    expected_orders = Schema(OrderWithCustomerDimension).create_dataframe(
        spark,
        [
            OrderWithCustomerDimension(
                order_id=1,
                customer_id="customer-1",
                order_timestamp=datetime(2026, 9, 24, 8, 30, tzinfo=UTC),
                product_id=100,
                quantity=2,
                name="Ada",
            )
        ],
    )
    path = tmp_path / "output"

    # When
    write_output(input_orders, OutputPath(str(path)))
    actual = spark.read.parquet(str(path))

    # Then
    assertDataFrameEqual(actual, expected_orders)
