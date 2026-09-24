from typing import Annotated

from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression, LinearRegressionModel
from pyspark.sql import DataFrame, SparkSession
from spark_joinery import Context, Project, ProjectCast, transform

from .context import HousingPath
from .schemas import Housing, HousingWithFeatures

FEATURE_COLUMNS = ["number_of_bedrooms", "square_footage"]


@transform
def read_data(
    spark: SparkSession, path: Annotated[HousingPath, Context()]
) -> Annotated[DataFrame, ProjectCast(Housing)]:
    return spark.read.parquet(path)


@transform
def prepare_features(
    housing: Annotated[DataFrame, Project(Housing)],
) -> Annotated[DataFrame, ProjectCast(HousingWithFeatures)]:
    return VectorAssembler(inputCols=FEATURE_COLUMNS, outputCol="features").transform(
        housing
    )


@transform
def fit_model(
    prepared_housing: Annotated[DataFrame, Project(HousingWithFeatures)],
) -> LinearRegressionModel:
    return LinearRegression(featuresCol="features", labelCol="price").fit(
        prepared_housing
    )


@transform
def print_coefficients(model: LinearRegressionModel) -> None:
    print(f"coefficients: {model.coefficients}")
    print(f"intercept: {model.intercept}")
