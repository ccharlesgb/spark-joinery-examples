from dataclasses import dataclass
from typing import Annotated

from pyspark.ml.linalg import Vector, VectorUDT


@dataclass
class Housing:
    number_of_bedrooms: int
    square_footage: int
    price: float


@dataclass
class HousingWithFeatures(Housing):
    features: Annotated[Vector, VectorUDT()]
