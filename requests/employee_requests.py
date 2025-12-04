from sqlmodel import Session, select
from db import engine
from models.employee import Employee
from models.schedule import Schedule

def get_all_staff():
    with Session(engine) as session:
        return session.exec(select(Employee)).all()

def add_schedule(employee_id: int, date: str, shift_time: str, position: str):
    with Session(engine) as session:
        schedule = Schedule(
            employee_id=employee_id,
            date=date,
            shift_time=shift_time,
            position=position
        )
        session.add(schedule)
        session.commit()
        return {"status": "смена добавлена"}
