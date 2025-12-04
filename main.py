from fastapi import FastAPI
from sqlmodel import Session, select
from db import engine
from models.guest import Guest
from models.room import Room
from models.booking import Booking
from models.service import Service
from models.invoice import Invoice
from models.invoice_service import InvoiceService
from models.employee import Employee
from models.schedule import Schedule

app = FastAPI()

# Guests
@app.get("/guests")
def get_guests():
    with Session(engine) as session:
        return session.exec(select(Guest)).all()

# Free Rooms
@app.get("/rooms/free")
def free_rooms():
    with Session(engine) as session:
        return session.exec(select(Room).where(Room.status == "свободен")).all()

# Create Booking
@app.post("/booking/create")
def create_booking(guest_id: int, room_id: int, check_in: str, check_out: str):
    with Session(engine) as session:
        booking = Booking(guest_id=guest_id, room_id=room_id, check_in=check_in, check_out=check_out, status="подтверждено", payment_method="карта")
        session.add(booking)
        room = session.get(Room, room_id)
        room.status = "забронирован"
        session.commit()
        return {"booking_id": booking.id, "room_status": room.status}

# Check-in
@app.post("/checkin")
def check_in(booking_id: int):
    with Session(engine) as session:
        booking = session.get(Booking, booking_id)
        room = session.get(Room, booking.room_id)
        room.status = "занят"
        session.commit()
        return {"room_status": room.status}

# Add Service
@app.post("/service/add")
def add_service(invoice_id: int, service_id: int, quantity: int = 1):
    with Session(engine) as session:
        inv_service = InvoiceService(invoice_id=invoice_id, service_id=service_id, quantity=quantity)
        session.add(inv_service)
        session.commit()
        return {"status": "услуга добавлена"}

# Checkout
@app.post("/checkout")
def checkout(booking_id: int):
    with Session(engine) as session:
        booking = session.get(Booking, booking_id)
        room = session.get(Room, booking.room_id)
        room.status = "требует уборки"
        invoice = session.exec(select(Invoice).where(Invoice.guest_id == booking.guest_id)).first()
        invoice.status = "оплачено"
        session.commit()
        return {"room_status": room.status, "invoice_status": invoice.status}

# Staff
@app.get("/staff")
def get_staff():
    with Session(engine) as session:
        return session.exec(select(Employee)).all()

# Schedule
@app.post("/schedule/add")
def add_schedule(employee_id: int, date: str, shift_time: str, position: str):
    with Session(engine) as session:
        schedule = Schedule(employee_id=employee_id, date=date, shift_time=shift_time, position=position)
        session.add(schedule)
        session.commit()
        return {"status": "смена добавлена"}
