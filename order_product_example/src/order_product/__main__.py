from pyspark.sql import SparkSession
from spark_joinery.dependencies import PipelineContext

from .context import CustomersPath, OrdersPath, OutputPath, RunDate
from .pipeline import DATA_DIR, OUTPUT_DIR, build_pipeline

spark = (
    SparkSession.builder.appName("order-product-pipeline")
    .master("local[*]")
    .getOrCreate()
)

pipeline = build_pipeline()
context = PipelineContext(
    values=[
        OrdersPath(str(DATA_DIR / "orders.parquet")),
        CustomersPath(str(DATA_DIR / "customers.parquet")),
        OutputPath(str(OUTPUT_DIR / "output.parquet")),
        RunDate(2026, 1, 1),
    ]
)
outputs = pipeline.run(spark, context)
outputs["join_orders_with_customers"].show()

spark.stop()
