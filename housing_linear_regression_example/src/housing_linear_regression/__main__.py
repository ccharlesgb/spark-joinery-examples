from pyspark.sql import SparkSession
from spark_joinery.dependencies import PipelineContext

from .context import HousingPath
from .pipeline import DATA_DIR, build_pipeline

spark = (
    SparkSession.builder.appName("housing-linear-regression-pipeline")
    .master("local[*]")
    .getOrCreate()
)

pipeline = build_pipeline()
context = PipelineContext(values=[HousingPath(str(DATA_DIR / "housing.parquet"))])
pipeline.run(spark, context)

spark.stop()
