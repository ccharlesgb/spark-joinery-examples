from collections.abc import Generator

import pytest
from housing_linear_regression.schemas import Housing
from housing_linear_regression.transform import fit_model, prepare_features
from pyspark.sql import SparkSession
from spark_joinery import Schema


@pytest.fixture(scope="session")
def spark() -> Generator[SparkSession]:
    session = (
        SparkSession.builder.master("local[1]")
        .appName("housing-linear-regression-transform-tests")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_fit_model_learns_housing_feature_coefficients(spark: SparkSession):
    housing = Schema(Housing).create_dataframe(
        spark,
        [
            Housing(1, 100, 250.0),
            Housing(2, 100, 350.0),
            Housing(1, 200, 450.0),
            Housing(2, 200, 550.0),
        ],
    )

    model = fit_model(prepare_features(housing))

    assert model.coefficients.toArray()[0] == pytest.approx(100.0)
    assert model.coefficients.toArray()[1] == pytest.approx(2.0)
    assert model.intercept == pytest.approx(-50.0)
