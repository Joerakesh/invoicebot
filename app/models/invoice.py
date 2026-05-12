from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy import Boolean
from sqlalchemy import DateTime

from datetime import datetime

from app.database.db import Base


class Invoice(Base):

    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)

    company = Column(String)

    invoice_no = Column(String, unique=True)

    invoice_date = Column(String)

    vat = Column(Float)

    total = Column(Float)

    currency = Column(String)

    source = Column(String)

    confidence = Column(Float)

    filename = Column(String)

    duplicate_invoice = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)