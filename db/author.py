from db.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Authors(Model):
    __tablename__ = "authors"

    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column(unique=True)
    biography: Mapped[str | None] = mapped_column(nullable=True)
    composition : Mapped[str | None] = mapped_column(nullable=True)

    books = relationship("Books",back_populates="author", cascade="all, delete-orphan")