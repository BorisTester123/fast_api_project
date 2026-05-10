from sqlalchemy import Table, Column, Integer, ForeignKey
from db.database import Base

author_book: Table = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey('authors.author_id'), primary_key=True),
    Column("book_id", Integer, ForeignKey('books.book_id'), primary_key=True)
)