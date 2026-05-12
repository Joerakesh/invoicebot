from app.connectors.local import LocalConnector


class Dispatcher:

    def __init__(self):

        self.connectors = [
            LocalConnector()
        ]

    def run(self):

        files = []

        for connector in self.connectors:

            connector_files = connector.fetch()

            files.extend(connector_files)

        return files