from sqlmodel import Session, select
from db import engine
from models.room import Room

def get_free_rooms():
    with Session(engine) as session:
        return session.exec(select(Room).where(Room.status == "свободен")).all()

def change_room_status(room_id: int, new_status: str):
    with Session(engine) as session:
        room = session.get(Room, room_id)
        if room:
            room.status = new_status
            session.commit()
        return room
