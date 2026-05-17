from app.utils.pdf_reader import read_pdf
from app.ai.extractor import extract_invoice
from app.services.excel_service import save_excel
from app.utils.file_handler import move_processed


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

    data["source"] = source

    save_excel(
        "storage/exports",
        data
    )

    print("EXCEL UPDATED")

    move_processed(file_path)

    print("FILE MOVED")