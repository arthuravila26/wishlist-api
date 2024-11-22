from typing import Union

from pydantic import BaseModel


class User(BaseModel):
    id: Union[int, None]
    name: Union[str, None]
    email: Union[str, None]
    wishlist: Union[list, None]


class CreateUser(BaseModel):
    name: Union[str, None]
    email: Union[str, None]
    password: Union[str, None]


class UserLogin(BaseModel):
    email: Union[str, None]
    password: Union[str, None]


class UpdateUser(BaseModel):
    name: Union[str, None]
    email: Union[str, None]
    password: Union[str, None]
