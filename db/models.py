from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Model

# Модель книги в базе данных
class Books(Model):
    # Название таблицы в базе данных
    __tablename__ = "books"

    # Уникальный идентификатор книги (первичный ключ)
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    # Название книги (обязательно для заполнения)
    name: Mapped[str]
    # Описание книги
    description: Mapped[str | None]
    author_id : Mapped[int]

    relationship("author", back_populates='authors')
