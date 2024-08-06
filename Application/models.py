from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from Application import db

class User(db.Model): # type: ignore
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, init=True)
    name: Mapped[str] = mapped_column(String(16), nullable=False, init=True)