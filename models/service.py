from sqlmodel import SQLModel, Field
from typing import Optional

class Service(SQLModel, table=True):
    __tablename__ = "service"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: Optional[float] = None
