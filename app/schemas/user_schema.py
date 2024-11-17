from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    name: Union[str, None]
    email: Union[str, None]
