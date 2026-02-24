from typing import Optional
from pydantic import BaseModel
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Book(BaseModel):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    cover_image_id: Optional[str] = None
    file_id: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
