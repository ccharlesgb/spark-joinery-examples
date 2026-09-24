from pathlib import Path

from spark_joinery.pipeline import Pipeline

from .transform import fit_model, prepare_features, print_coefficients, read_data

DATA_DIR = Path(__file__).parent.parent.parent / "data"


def build_pipeline() -> Pipeline:
    pipeline = Pipeline()
    housing = pipeline.add_step(read_data)
    prepared_housing = pipeline.add_step(prepare_features)
    model = pipeline.add_step(fit_model)
    coefficients = pipeline.add_step(print_coefficients)

    pipeline.connect(housing, prepared_housing)
    pipeline.connect(prepared_housing, model)
    pipeline.connect(model, coefficients)

    return pipeline
