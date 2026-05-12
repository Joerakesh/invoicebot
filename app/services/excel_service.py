import os

from openpyxl import Workbook
from openpyxl import load_workbook

FILE_NAME = "Invoices_Master.xlsx"


def save_excel(base_path, data):

    os.makedirs(
        base_path,
        exist_ok=True
    )

    file_path = os.path.join(
        base_path,
        FILE_NAME
    )

    sheet_name = data["company"][:31]

    row = [
        data["invoice_no"],
        data["date"],
        data["company"],
        data["total"],
        data["vat"],
        data["currency"],
        data["source"],
        data["confidence"]
    ]

    if not os.path.exists(file_path):

        wb = Workbook()

        ws = wb.active

        ws.title = sheet_name

        ws.append([
            "Invoice No",
            "Date",
            "Company",
            "Total",
            "VAT",
            "Currency",
            "Source",
            "Confidence"
        ])

        ws.append(row)

        wb.save(file_path)

        return

    wb = load_workbook(file_path)

    if sheet_name not in wb.sheetnames:

        ws = wb.create_sheet(title=sheet_name)

        ws.append([
            "Invoice No",
            "Date",
            "Company",
            "Total",
            "VAT",
            "Currency",
            "Source",
            "Confidence"
        ])

    else:

        ws = wb[sheet_name]

    ws.append(row)

    wb.save(file_path)