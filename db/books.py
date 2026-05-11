from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.author_book import author_book
from sqlalchemy import DateTime, func, ForeignKey, Date
from datetime import datetime, date
from sqlalchemy import Enum as SQLEnum
from enums.enum import CountryCode


class Book(Base):
    __tablename__ = "books"


    book_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(
        unique=True,
        nullable=False
    )
    title: Mapped[str] = mapped_column(unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)

    language_code : Mapped[CountryCode] = mapped_column(
        SQLEnum(CountryCode),
        nullable=False
    )

    publication_date : Mapped[date] = mapped_column(Date)
    page_count : Mapped[int] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at : Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    deleted_at : Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    created_by : Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        server_default='1'
    )

    updated_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        server_default='1'
    )

    authors = relationship("Author", secondary=author_book, back_populates="books", passive_deletes=True)
