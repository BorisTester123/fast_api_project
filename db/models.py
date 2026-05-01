from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db.database import Model

class Books(Model):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id", ondelete="CASCADE"))
    name: Mapped[str | None] = mapped_column(nullable=True, unique=True)
    description: Mapped[str | None] = mapped_column(nullable=True)

    author = relationship("Authors", back_populates="books", passive_deletes=True)
