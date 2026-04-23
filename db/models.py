from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Model

# Модель книги в базе данных
class Books(Model):
    # Название таблицы в базе данных
    __tablename__ = "books"

    # Уникальный идентификатор книги (первичный ключ)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # ID автора
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"))
    # Название книги (обязательно для заполнения)
    name: Mapped[str | None] = mapped_column(nullable=True)
    # Описание книги
    description: Mapped[str | None] = mapped_column(nullable=True)

    author = relationship("Authors", back_populates="books")
