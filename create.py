import asyncio
import os
from dotenv import load_dotenv
from sqlalchemy import select

from db.database import async_session
from db.models import User
from utils.util import hash_password

load_dotenv()

async def create_admin_if_not_exists():
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_password:
        raise ValueError("ADMIN_PASSWORD не задан в .env файле!")

    async with async_session() as db:
        result = await db.execute(
            select(User).where(User.username == admin_username)
        )
        if result.scalar_one_or_none():
            return

        hashed = hash_password(admin_password)

        admin = User(username=admin_username, password_hash=hashed)
        db.add(admin)
        await db.commit()
        await db.refresh(admin)

if __name__ == "__main__":
    asyncio.run(create_admin_if_not_exists())