from sqlalchemy import ForeignKey
from db.database import Model
from sqlalchemy.orm import Mapped, mapped_column


class Authors(Model):
    __tablename__ = "authors"

    id : Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    author : Mapped[str]
    composition : Mapped[str | None]

    author_id : Mapped[int] = mapped_column(ForeignKey("books.id"))