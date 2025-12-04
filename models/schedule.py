from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Schedule(SQLModel, table=True):
    __tablename__ = "schedule"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    employee_id: int = Field(foreign_key="LiSasha.employee.id")
    date: date
    shift_time: Optional[str] = None
    position: Optional[str] = None
