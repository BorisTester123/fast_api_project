from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import bcrypt
from sqlalchemy import select

from db.database import async_session
from db.models import User


security = HTTPBasic()


async def check_auth(
    credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Проверяет Basic Auth по данным из базы.
    Возвращает username, если авторизация прошла успешно.
    """
    async with async_session() as db:
        # Ищем пользователя по username
        result = await db.execute(
            select(User).where(User.username == credentials.username)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Basic"},
            )

        # Проверяем пароль с помощью bcrypt
        if not bcrypt.checkpw(
            credentials.password[:72].encode("utf-8"),
            user.password_hash.encode("utf-8")
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Basic"},
            )

        return credentials.username   # или можно возвращать весь user, если понадобится