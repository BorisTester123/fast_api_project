from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.author_book import author_book


class Author(Base):
    __tablename__ = "authors"

    author_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name : Mapped[str] = mapped_column(unique=True)
    biography: Mapped[str | None] = mapped_column(nullable=True)
    composition : Mapped[str | None] = mapped_column(nullable=True)

    books = relationship("Book", secondary=author_book, back_populates="authors")