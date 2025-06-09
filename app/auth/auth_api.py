from fastapi import APIRouter, Form, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials
from tortoise.exceptions import IntegrityError

from app.logger_config import setup_logger
from app.schemas.users import UserCreate, UserOut
from app.security.jwt_auth import (
    bearer_scheme,
    create_access_token,
    create_refresh_token,
    decode_token,
    hash_password,
    verify_password,
)
from db.models import Users

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

logger = setup_logger(__name__)


@auth_router.post(
    "/register",
    response_model=UserOut,
    summary="Регистрация",
    description="Создание новой учетной записи на основе `email` и `password` ",
)
async def register_user(user: UserCreate):
    hashed_pwd = hash_password(user.password)

    try:
        user_obj = await Users.create(email=user.email, password=hashed_pwd)
        logger.info("Зарегистрирован новый пользователь!")
    except IntegrityError:
        raise HTTPException(
            status_code=400, detail="Пользователь с таким email уже существует"
        )

    return user_obj


@auth_router.post(
    "/token",
    summary="Получение JWT токенов",
    description="Эндпоинт для получение `access_token` и `refresh_token`",
)
async def login_for_access_token(email: str = Form(...), password: str = Form(...)):
    user = await Users.get_or_none(email=email)
    if not user or not verify_password(password, user.password):
        logger.warning("Попытка входа с невалидными данными")
        raise HTTPException(status_code=401, detail="Неверные данные для входа")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@auth_router.post("/refresh", summary="Обновление access_token")
async def get_refresh_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_scheme),
):
    user_id = decode_token(credentials.credentials)
    new_access_token = create_access_token(data={"sub": user_id})
    return {"access_token": new_access_token, "token_type": "bearer"}
