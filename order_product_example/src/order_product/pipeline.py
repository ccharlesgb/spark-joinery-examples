from pathlib import Path

from spark_joinery.pipeline import Pipeline

from .transform import (
    filter_orders,
    join_orders_with_customers,
    read_customers,
    read_orders,
    write_output,
)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "__output"


def build_pipeline() -> Pipeline:
    pipeline = Pipeline()
    orders = pipeline.add_step(read_orders)
    filtered_orders = pipeline.add_step(filter_orders)
    customers = pipeline.add_step(read_customers)
    joined = pipeline.add_step(join_orders_with_customers)
    output = pipeline.add_step(write_output)

    pipeline.connect(orders, filtered_orders)
    pipeline.connect(filtered_orders, joined)
    pipeline.connect(customers, joined)
    pipeline.connect(joined, output)

    return pipeline
