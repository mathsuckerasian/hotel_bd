from sqlmodel import Session
from db import engine
from models.booking import Booking
from models.room import Room

def create_booking(guest_id: int, room_id: int, check_in, check_out, payment_method="карта"):
    with Session(engine) as session:
        booking = Booking(
            guest_id=guest_id,
            room_id=room_id,
            check_in=check_in,
            check_out=check_out,
            status="подтверждено",
            payment_method=payment_method
        )
        session.add(booking)
        
        # Меняем статус номера
        room = session.get(Room, room_id)
        room.status = "забронирован"
        
        session.commit()
        session.refresh(booking)
        return booking

def check_in_booking(booking_id: int):
    with Session(engine) as session:
        booking = session.get(Booking, booking_id)
        room = session.get(Room, booking.room_id)
        room.status = "занят"
        session.commit()
        return room
