from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text


class Base(DeclarativeBase):
    pass


class Recipe(Base):
    __tablename__ = "recipes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(String(200), index=True)
    cooking_time: Mapped[int] = mapped_column(Integer)  # минуты
    views: Mapped[int] = mapped_column(Integer, default=0)

    ingredients: Mapped[str] = mapped_column(Text)
    description: Mapped[str] = mapped_column(Text)
