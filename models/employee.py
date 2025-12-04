from sqlmodel import SQLModel, Field
from typing import Optional

class Employee(SQLModel, table=True):
    __tablename__ = "employee"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str
    role: Optional[str] = None
    phone: Optional[str] = None
