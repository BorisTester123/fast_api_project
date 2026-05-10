from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Base
from db.author_book import author_book

class Book(Base):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)

    authors = relationship("Author", secondary=author_book, back_populates="books", passive_deletes=True)
