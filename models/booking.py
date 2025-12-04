from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Booking(SQLModel, table=True):
    __tablename__ = "booking"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    guest_id: int = Field(foreign_key="LiSasha.guest.id")
    room_id: int = Field(foreign_key="LiSasha.room.id")
    check_in: date
    check_out: date
    status: Optional[str] = None
    payment_method: Optional[str] = None
