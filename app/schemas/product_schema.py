from pydantic import BaseModel
from typing import Union

class Product(BaseModel):
    title: Union[str, None]
    price: Union[float, None]
    brand: Union[str, None]
    image: Union[str, None]
    reviewScore: Union[float, None]
