from pathlib import Path

from spark_joinery.pipeline import Pipeline

from .transform import (
    denormalise_group_id,
    read_customers,
    write_output,
)

DATA_DIR = Path(__file__).parent.parent.parent / "data"
OUTPUT_DIR = Path(__file__).parent.parent.parent / "__output"


def build_pipeline() -> Pipeline:
    pipeline = Pipeline()

    read_customers_step = pipeline.add_step(read_customers, "read_customers")
    denormalise_group_id_step = pipeline.add_step(
        denormalise_group_id, "denormalise_group_id"
    )
    write_output_step = pipeline.add_step(write_output, "write_output")

    pipeline.connect(read_customers_step, denormalise_group_id_step)
    pipeline.connect(denormalise_group_id_step, write_output_step)

    return pipeline
