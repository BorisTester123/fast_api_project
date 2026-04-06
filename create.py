# create_admin.py
# -*- coding: utf-8 -*-
import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import select

from db.database import async_session
from db.models import User
from utils.util import hash_password

# Загружаем креды из .env
load_dotenv()

async def create_admin_if_not_exists():
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "password")  # дефолт на случай отсутствия

    async with async_session() as db:
        # Проверяем, есть ли уже пользователь
        result = await db.execute(select(User).where(User.username == admin_username))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            print(f"Admin user '{admin_username}' уже существует")
            return

        # Хэшируем пароль
        hashed = hash_password(admin_password)

        # Создаём админа
        admin = User(username=admin_username, password_hash=hashed)
        db.add(admin)
        await db.commit()
        await db.refresh(admin)

        print(f"Admin user '{admin_username}' создан успешно!")

if __name__ == "__main__":
    asyncio.run(create_admin_if_not_exists())
