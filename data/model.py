from typing import List

from sqlalchemy import ForeignKey, Column, Integer, Table
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


association_table = Table(
    "articles_categories",
    Base.metadata,
    Column("article_id", Integer, ForeignKey("article.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)


class Category(Base):
    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    def __repr__(self) -> str:
        return f"Category(id={self.id}, name={self.name})"


class Article(Base):
    __tablename__ = 'article'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    origin: Mapped[str]

    categories: Mapped[List[Category]] = relationship(secondary=association_table)

    def __repr__(self) -> str:
        return f"Article(id={self.id}, title={self.title}, content={self.content})"
