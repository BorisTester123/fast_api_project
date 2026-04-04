from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from schema.user_create import UserCreate, UserRead
from utils.util import hash_password
from sqlalchemy import select
from db.database import async_session
from db.models import User

# Создаем роутер для группировки endpoints связанных с операциями
router = APIRouter(
    # Присваиваем тэг и префикс для нашей документации API
    prefix="/register"
)

async def get_db():
    async with async_session() as session:
        yield session

# Создаем ручку для создания и чтения моделей UserCreate, UserRead.
@router.post("", response_model=UserRead)
async def create(user: UserCreate, db: AsyncSession = Depends(get_db)):
    # передаем в нашу функцию сессию, и создаем юзера, проверяем что такой username существует в базе
    result = await db.execute(select(User).where(User.username == user.username))
    existing_user = result.scalar_one_or_none()
    # если такого юзера в базе нет, возвращаем ошибку
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    # если есть, хэшируем пароль.
    hashed_password = hash_password(user.password)
    # указываем какое поле будет захэшировано.
    new_user = User(username=user.username, password_hash=hashed_password)
    # добавляем креды для авторизации в swagger, уже захэшированные данные.
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return UserRead(id=new_user.id, username=new_user.username)