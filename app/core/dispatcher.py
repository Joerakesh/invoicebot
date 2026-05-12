from app.connectors.whatsapp import WhatsAppConnector
from app.connectors.gmail import GmailConnector


class Dispatcher:

    def __init__(self):

        self.connectors = [
            GmailConnector(),
        ]

    def run(self):

        files = []

        for connector in self.connectors:

            try:

                files.extend(
                    connector.fetch()
                )

            except Exception as e:

                print(
                    "CONNECTOR ERROR:",
                    str(e)
                )

        return files