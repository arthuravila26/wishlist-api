from datetime import timedelta

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.authentication import authenticate_user, create_access_token
from app.db.database import get_db
from app.schemas.token_schema import UserLogin

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/token")
def login_for_access_token(request: UserLogin, session: Session = Depends(get_db)):
    user = authenticate_user(request.email, request.password, session)
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"Authorization": f"Bearer {access_token}"}
