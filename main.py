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
from fastapi import FastAPI, HTTPException

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

# Soft Delete Utility
def soft_delete(session, model, record_id: int):
    obj = session.get(model, record_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Объект id={record_id} не найден")
    if getattr(obj, "status", None) == "deleted":
        raise HTTPException(status_code=400, detail="Запись уже удалена")
    obj.status = "deleted"
    session.add(obj)
    session.commit()
    return {"ok": True, "message": f"Запись id={record_id} помечена как удалённая"}

def restore_record(session, model, record_id: int):
    obj = session.get(model, record_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"Объект id={record_id} не найден")
    if getattr(obj, "status", None) != "deleted":
        raise HTTPException(status_code=400, detail="Запись не удалена")
    obj.status = "active"
    session.add(obj)
    session.commit()
    return {"ok": True, "message": f"Запись id={record_id} восстановлена"}

# Guest Delete/Restore
@app.delete("/guests/{guest_id}")
def delete_guest(guest_id: int):
    with Session(engine) as session:
        return soft_delete(session, Guest, guest_id)

@app.put("/guests/{guest_id}/restore")
def restore_guest(guest_id: int):
    with Session(engine) as session:
        return restore_record(session, Guest, guest_id)

# Booking Delete/Restore
@app.delete("/booking/{booking_id}")
def delete_booking(booking_id: int):
    with Session(engine) as session:
        return soft_delete(session, Booking, booking_id)

@app.put("/booking/{booking_id}/restore")
def restore_booking(booking_id: int):
    with Session(engine) as session:
        return restore_record(session, Booking, booking_id)

# Room Delete/Restore
@app.delete("/rooms/{room_id}")
def delete_room(room_id: int):
    with Session(engine) as session:
        return soft_delete(session, Room, room_id)

@app.put("/rooms/{room_id}/restore")
def restore_room(room_id: int):
    with Session(engine) as session:
        return restore_record(session, Room, room_id)

# Service Delete/Restore
@app.delete("/service/{service_id}")
def delete_service(service_id: int):
    with Session(engine) as session:
        return soft_delete(session, Service, service_id)

@app.put("/service/{service_id}/restore")
def restore_service(service_id: int):
    with Session(engine) as session:
        return restore_record(session, Service, service_id)
    

@app.put("/guests/{guest_id}")
def update_guest(guest_id: int, updated_guest: Guest):
    with Session(engine) as session:
        guest = session.get(Guest, guest_id)
        if not guest or getattr(guest, "status", None) == "deleted":
            raise HTTPException(status_code=404, detail="Гость не найден или удалён")
        
        for key, value in updated_guest.dict(exclude_unset=True).items():
            setattr(guest, key, value)
        
        session.add(guest)
        session.commit()
        session.refresh(guest)
        return {"ok": True, "message": f"Гость id={guest_id} обновлён", "guest": guest}
    
# Generate Invoice
@app.post("/invoice/generate")
def generate_invoice(booking_id: int):
    with Session(engine) as session:
        booking = session.get(Booking, booking_id)
        if not booking:
            raise HTTPException(status_code=404, detail="Бронирование не найдено")

        guest_id = booking.guest_id

        room = session.get(Room, booking.room_id)
        if not room:
            raise HTTPException(status_code=404, detail="Комната не найдена")

        days = (booking.check_out - booking.check_in).days
        if days < 1:
            days = 1 

        room_cost = room.price_per_day * days

        invoice = session.exec(select(Invoice).where(Invoice.guest_id == guest_id)).first()
        if not invoice:
            invoice = Invoice(guest_id=guest_id, total_amount=0, status="не оплачено")
            session.add(invoice)
            session.flush() 

        inv_services = session.exec(select(InvoiceService).where(InvoiceService.invoice_id == invoice.id)).all()

        service_total = 0
        for item in inv_services:
            service_obj = session.get(Service, item.service_id)
            if service_obj:
                service_total += service_obj.price * item.quantity

        final_total = room_cost + service_total

        invoice.total_amount = final_total
        session.commit()
        session.refresh(invoice)

        return {
            "invoice_id": invoice.id,
            "guest_id": guest_id,
            "room_cost": room_cost,
            "service_cost": service_total,
            "total_amount": final_total,
            "status": invoice.status
        }
