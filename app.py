import time

from app.core.dispatcher import Dispatcher
from app.core.processor import process_invoice

from app.utils.file_handler import move_processed


print("APP STARTED")

dispatcher = Dispatcher()

while True:

    print("CHECKING FILES")

    files = dispatcher.run()

    print("FILES:", files)

    for file in files:

        print("PROCESSING:", file)

        process_invoice(
            file,
            "local"
        )

        move_processed(file)

        print("FILE MOVED")

    time.sleep(30)