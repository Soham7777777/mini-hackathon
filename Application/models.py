from Application import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class User(db.Model): # type: ignore
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    password: Mapped[str] = mapped_column(String(16))