import pdfplumber

from app.utils.logger import logger


def read_pdf(path: str):

    text = ""

    try:

        with pdfplumber.open(path) as pdf:

            for page in pdf.pages:

                extracted = page.extract_text()

                if extracted:
                    text += extracted + "\n"

        logger.info(f"PDF extracted: {path}")

        return text

    except Exception as e:

        logger.error(f"PDF read failed: {e}")

        return ""