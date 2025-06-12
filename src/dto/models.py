from enum import Enum
from pydantic import BaseModel


class ModelId(str, Enum):
    food_cls = "clothes-classification"


class PredictRequest(BaseModel):
    """
    모델 예측
    - url (str): 이미지 url
    """
    url: str
