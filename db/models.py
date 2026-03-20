from sqlalchemy.orm import Mapped, mapped_column
from db.database import Model

# Модель книги в базе данных
class BooksOrm(Model):
    # Название таблицы в базе данных
    __tablename__ = "books"

    # Уникальный идентификатор книги (первичный ключ)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Название книги (обязательно для заполнения)
    name: Mapped[str]
    # Автор книги
    author: Mapped[str | None]
    # Описание книги
    description: Mapped[str | None]