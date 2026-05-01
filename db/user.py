from sqlalchemy.orm import Mapped, mapped_column
from db.database import Model

class User(Model):
    __tablename__ = "users"

    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password_hash : Mapped[str] = mapped_column(nullable=False)
