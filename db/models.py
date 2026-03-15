from sqlalchemy.orm import Mapped, mapped_column
from db.database import Model

class BooksOrm(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    author: Mapped[str | None]
    description: Mapped[str | None]