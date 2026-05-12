import os

from app.utils.logger import logger


class LocalConnector:

    def __init__(self):

        self.folder = "storage/incoming"

    def fetch(self):

        files = []

        for file in os.listdir(self.folder):

            if file.endswith(".pdf"):

                full_path = os.path.join(
                    self.folder,
                    file
                )

                files.append(full_path)

        logger.info(f"LocalConnector found {len(files)} PDFs")

        return files