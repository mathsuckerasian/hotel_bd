from sqlmodel import SQLModel, Field
from typing import Optional

class Room(SQLModel, table=True):
    __tablename__ = "room"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    room_number: int
    type: Optional[str] = None
    price_per_day: Optional[float] = None
    status: Optional[str] = None
    capacity: Optional[int] = None
