from sqlmodel import SQLModel, Field
from typing import Optional

class InvoiceService(SQLModel, table=True):
    __tablename__ = "invoice_service"
    __table_args__ = {"schema": "LiSasha"}

    id: Optional[int] = Field(default=None, primary_key=True)
    invoice_id: int = Field(foreign_key="LiSasha.invoice.id")
    service_id: int = Field(foreign_key="LiSasha.service.id")
    quantity: int = Field(default=1)
