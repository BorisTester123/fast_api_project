from datetime import datetime
from db.database import Base
from sqlalchemy import DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.author_book import author_book


class Author(Base):
    __tablename__ = "authors"

    author_id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    original_name : Mapped[str] = mapped_column(unique=True)
    name : Mapped[str | None] = mapped_column(unique=True)

    biography: Mapped[str | None] = mapped_column(nullable=True)
    composition : Mapped[str | None] = mapped_column(nullable=True)

    birth_date : Mapped[str] = mapped_column(nullable=False)
    death_date : Mapped[str | None] = mapped_column(nullable=True)

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

    books = relationship("Book", secondary=author_book, back_populates="authors")