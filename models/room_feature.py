from sqlmodel import SQLModel, Field
from typing import Optional

class RoomFeature(SQLModel, table=True):
    __tablename__ = "room_feature"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    room_id: int = Field(foreign_key="LiSasha.room.id")
    feature: str
