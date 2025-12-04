from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Invoice(SQLModel, table=True):
    __tablename__ = "invoice"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    guest_id: int = Field(foreign_key="LiSasha.guest.id")
    total_amount: Optional[float] = None
    status: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.now)
