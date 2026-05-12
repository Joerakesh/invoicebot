import os

from app.utils.pdf_reader import read_pdf

from app.ai.extractor import extract_invoice

from app.services.excel_service import save_excel

from app.database.db import SessionLocal

from app.models.invoice import Invoice


def process_invoice(file_path, source):

    print(f"PROCESSING FROM {source}")

    text = read_pdf(file_path)

    if not text:

        print("EMPTY PDF")

        return

    data = extract_invoice(text)

    if not data:

        print("EXTRACTION FAILED")

        return

    db = SessionLocal()

    existing = db.query(Invoice).filter(
        Invoice.invoice_no == data["invoice_no"]
    ).first()

    if existing:

        print("DUPLICATE DETECTED")

        return

    invoice = Invoice(
        company=data.get("company"),
        invoice_no=data.get("invoice_no"),
        invoice_date=data.get("date"),
        vat=data.get("vat", 0),
        total=data.get("total", 0),
        currency=data.get("currency"),
        source=source,
        confidence=data.get("confidence", 0),
        filename=os.path.basename(file_path)
    )

    db.add(invoice)

    db.commit()

    save_excel(
        "storage/exports",
        {
            "company": invoice.company,
            "invoice_no": invoice.invoice_no,
            "date": invoice.invoice_date,
            "vat": invoice.vat,
            "total": invoice.total,
            "currency": invoice.currency,
            "source": invoice.source,
            "confidence": invoice.confidence
        }
    )

    print("DATABASE UPDATED")

    print("EXCEL UPDATED")