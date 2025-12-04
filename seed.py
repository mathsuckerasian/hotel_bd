from sqlmodel import Session
from db import engine
from models.guest import Guest
from models.room import Room
from models.room_feature import RoomFeature
from models.booking import Booking
from models.service import Service
from models.invoice import Invoice
from models.invoice_service import InvoiceService
from models.employee import Employee
from models.schedule import Schedule
from datetime import date

with Session(engine) as session:
    # Гости
    guest1 = Guest(full_name="Иван Иванов", passport="1234 567890", phone="+79990001122", email="ivan@example.com")
    guest2 = Guest(full_name="Мария Петрова", passport="2345 678901", phone="+79990003344", email="maria@example.com")
    session.add_all([guest1, guest2])
    session.commit()  # id присвоены
    session.refresh(guest1)
    session.refresh(guest2)

    # Номера
    room1 = Room(room_number=101, type="Одноместный", price_per_day=2500, status="свободен", capacity=1)
    room2 = Room(room_number=102, type="Двухместный", price_per_day=4000, status="свободен", capacity=2)
    session.add_all([room1, room2])
    session.commit()
    session.refresh(room1)
    session.refresh(room2)

    # Особенности номеров
    rf1 = RoomFeature(room_id=room1.id, feature="Pet-friendly")
    rf2 = RoomFeature(room_id=room2.id, feature="Вид на море")
    session.add_all([rf1, rf2])

    # Услуги
    service1 = Service(name="Завтрак", price=500)
    service2 = Service(name="Уборка", price=300)
    session.add_all([service1, service2])
    session.commit()
    session.refresh(service1)
    session.refresh(service2)

    # Сотрудники
    emp1 = Employee(full_name="Алексей Смирнов", role="администратор", phone="+79991112233")
    emp2 = Employee(full_name="Елена Кузнецова", role="горничная", phone="+79991113344")
    session.add_all([emp1, emp2])
    session.commit()
    session.refresh(emp1)
    session.refresh(emp2)

    # Расписание
    sch1 = Schedule(employee_id=emp1.id, date=date.today(), shift_time="08:00-16:00", position="Ресепшен")
    sch2 = Schedule(employee_id=emp2.id, date=date.today(), shift_time="08:00-16:00", position="Уборка")
    session.add_all([sch1, sch2])

    # Создание бронирования
    booking1 = Booking(
        guest_id=guest1.id,
        room_id=room1.id,
        check_in=date.today(),
        check_out=date.today(),
        status="подтверждено",
        payment_method="карта"
    )
    session.add(booking1)
    session.commit()
    session.refresh(booking1)

    # Счёт и услуги
    invoice1 = Invoice(
        guest_id=guest1.id,
        total_amount=3000,
        status="не оплачено"
    )
    session.add(invoice1)
    session.commit()
    session.refresh(invoice1)

    invoice_service1 = InvoiceService(
        invoice_id=invoice1.id,
        service_id=service1.id,
        quantity=1
    )
    session.add(invoice_service1)
    session.commit()

print("Seed данные созданы")
