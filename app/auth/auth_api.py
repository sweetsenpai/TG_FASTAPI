from fastapi import APIRouter, Form, HTTPException
from tortoise.exceptions import IntegrityError

from app.logger_config import setup_logger
from app.schemas.users import UserCreate, UserOut
from app.security.jwt_auth import create_access_token, hash_password, verify_password
from db.models import Users

user_router = APIRouter(prefix="/auth", tags=["Auth"])

logger = setup_logger(__name__)


@user_router.post("/register", response_model=UserOut)
async def register_user(user: UserCreate):
    hashed_pwd = hash_password(user.password)

    try:
        user_obj = await Users.create(email=user.email, password=hashed_pwd)
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    return user_obj


@user_router.post("/token")
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    user = await Users.get_or_none(email=email)
    if not user or not verify_password(password, user.password):
        logger.warning("Попытка входа с невалидными данными")
        raise HTTPException(status_code=401, detail="Неверные данные")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
