from sqlalchemy import Integer, String, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from Application import db
from decimal import Decimal

class Product(db.Model): 
    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False, init=True)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=10, scale=2), nullable=False, init=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, init=True)
    rating: Mapped[int] = mapped_column(Integer, nullable=True, init=True)
    description: Mapped[str] = mapped_column(String(50), nullable=True, init=True)
    company: Mapped[str] = mapped_column(String(100), nullable=True, init=True)