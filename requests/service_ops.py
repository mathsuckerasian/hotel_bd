from sqlmodel import Session
from db import engine
from models.invoice_service import InvoiceService

def add_service_to_invoice(invoice_id: int, service_id: int, quantity: int = 1):
    with Session(engine) as session:
        inv_service = InvoiceService(
            invoice_id=invoice_id,
            service_id=service_id,
            quantity=quantity
        )
        session.add(inv_service)
        session.commit()
        return {"status": "услуга добавлена"}
