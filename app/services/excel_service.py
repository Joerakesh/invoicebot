import os

from openpyxl import Workbook, load_workbook

EXPORT_FILE = "storage/exports/Invoices.xlsx"


def invoice_exists(ws, invoice_no):

    for row in ws.iter_rows(min_row=2):

        cell_value = row[0].value

        if cell_value == invoice_no:
            return True

    return False


def save_invoice(data: dict):

    row = [
        data["invoice_no"],
        data["company"],
        data["date"],
        data["currency"],
        data["vat"],
        data["total"],
        data["confidence"]
    ]

    if not os.path.exists(EXPORT_FILE):

        wb = Workbook()

        ws = wb.active

        ws.title = "Invoices"

        ws.append([
            "Invoice No",
            "Company",
            "Date",
            "Currency",
            "VAT",
            "Total",
            "Confidence"
        ])

        ws.append(row)

        wb.save(EXPORT_FILE)

        return True

    wb = load_workbook(EXPORT_FILE)

    ws = wb.active

    if invoice_exists(
        ws,
        data["invoice_no"]
    ):

        print("DUPLICATE INVOICE SKIPPED")

        return False

    ws.append(row)

    wb.save(EXPORT_FILE)

    return True