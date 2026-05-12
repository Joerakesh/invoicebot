import time

from app.core.dispatcher import Dispatcher
from app.utils.pdf_reader import read_pdf
from app.ai.extractor import extract_invoice
from app.utils.file_handler import move_processed
from app.services.excel_service import save_invoice
from app.utils.invoice_cleaner import clean_invoice_text

print("APP STARTED")

dispatcher = Dispatcher()

while True:

    print("CHECKING FILES")

    files = dispatcher.run()

    print("FILES:", files)

    for file in files:

        print("PROCESSING:", file)

        text = read_pdf(file)

        print("PDF TEXT LENGTH:", len(text))

        cleaned_text = clean_invoice_text(text)

        print(cleaned_text)

        data = extract_invoice(cleaned_text)

        print("AI RESPONSE:", data)

        if data:
            saved = save_invoice(data)

            if saved:
                print("EXCEL UPDATED")
            else:
                print("DUPLICATE DETECTED")
            
            move_processed(file)
            
            print("FILE MOVED")

    time.sleep(30)