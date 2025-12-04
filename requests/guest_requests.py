from sqlmodel import Session, select
from db import engine
from models.guest import Guest

def get_all_guests():
    with Session(engine) as session:
        return session.exec(select(Guest)).all()

def create_guest(full_name: str, passport: str = None, phone: str = None, email: str = None):
    with Session(engine) as session:
        guest = Guest(full_name=full_name, passport=passport, phone=phone, email=email)
        session.add(guest)
        session.commit()
        session.refresh(guest)
        return guest
