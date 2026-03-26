import asyncio
from sqlalchemy.future import select
from db.database import async_session
from db.models import User
from utils.util import hash_password

async def create_admin_if_not_exists():
    async with async_session() as db:
        # Проверяем, есть ли admin
        result = await db.execute(select(User).where(User.username == "admin"))
        admin = result.scalar_one_or_none()

        if admin:
            print("Admin уже существует")
            return

        # Создаём admin
        hashed = hash_password("testtest")  # хешируем безопасно для bcrypt
        admin = User(username="admin", password_hash=hashed)
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        print(f"Admin создан с id={admin.id}")

if __name__ == "__main__":
    asyncio.run(create_admin_if_not_exists())
