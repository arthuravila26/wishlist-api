from typing import Union

from pydantic import BaseModel


class Product(BaseModel):
    title: Union[str, None]
    price: Union[float, None]
    brand: Union[str, None]
    image: Union[str, None]
    reviewScore: Union[float, None]
