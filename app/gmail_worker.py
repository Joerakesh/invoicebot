import time

from app.connectors.gmail import GmailConnector

from app.core.processor import process_invoice

from app.utils.file_handler import move_processed


print("GMAIL WORKER STARTED")


gmail = GmailConnector()


while True:

    try:

        print("CHECKING GMAIL...")

        files = gmail.fetch_invoices()

        print("FILES FOUND:", files)

        for file in files:

            process_invoice(
                file,
                "gmail"
            )

            move_processed(file)

            print("FILE MOVED")

    except Exception as e:

        print("GMAIL WORKER ERROR:", str(e))

    time.sleep(600)