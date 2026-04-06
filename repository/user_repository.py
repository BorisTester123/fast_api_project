from db.database import async_session
from sqlalchemy import select
from db.user import User


class UserRepository:

    @classmethod
    async def find_by_user(cls, username : str):
        async with async_session() as session:
            async with session.begin():
                result = await session.execute(
                    select(User).where(User.username == username)
                )
                return result.scalar_one_or_none()