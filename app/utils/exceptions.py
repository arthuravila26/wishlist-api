from fastapi import HTTPException


class UserNotFound(HTTPException):
    def __init__(self, msg: str = 'User not found.'):
        super().__init__(detail=msg, status_code=422)

class EmailAlreadyExists(HTTPException):
    def __init__(self, msg: str = 'This email is already registered.'):
        super().__init__(detail=msg, status_code=400)
