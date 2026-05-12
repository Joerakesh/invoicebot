import os
import shutil

from app.utils.logger import logger


def move_processed(file_path: str):

    destination = os.path.join(
        "storage/processed",
        os.path.basename(file_path)
    )

    shutil.move(
        file_path,
        destination
    )

    logger.info(
        f"Moved file to processed: {destination}"
    )