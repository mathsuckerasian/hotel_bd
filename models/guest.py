from sqlmodel import SQLModel, Field
from typing import Optional

class Guest(SQLModel, table=True):
    __tablename__ = "guest"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    passport: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
