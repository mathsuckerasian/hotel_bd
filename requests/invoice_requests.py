from sqlmodel import Session, select
from db import engine
from models.invoice import Invoice

def create_invoice(guest_id: int, total_amount: float, status="не оплачено"):
    with Session(engine) as session:
        invoice = Invoice(guest_id=guest_id, total_amount=total_amount, status=status)
        session.add(invoice)
        session.commit()
        session.refresh(invoice)
        return invoice

def get_invoice_by_guest(guest_id: int):
    with Session(engine) as session:
        return session.exec(select(Invoice).where(Invoice.guest_id == guest_id)).first()
