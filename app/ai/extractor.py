import json

from google import genai

from app.config.settings import settings
from app.utils.logger import logger


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def extract_invoice(text: str):

    prompt = f"""
Extract invoice information from this invoice text.

Return ONLY valid JSON.

Format:

{{
  "company": "",
  "invoice_no": "",
  "date": "",
  "currency": "",
  "vat": 0,
  "total": 0,
  "confidence": 0.0
}}

Invoice Text:
{text[:4000]}
"""

    try:

        print("CALLING GEMINI")

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )
        print("GEMINI RESPONSE RECEIVED")
        content = response.text.strip()

        content = content.replace(
            "```json",
            ""
        ).replace(
            "```",
            ""
        )

        data = json.loads(content)

        logger.info(
            f"Invoice extracted: {data}"
        )

        return data

    except Exception as e:

        logger.error(
            f"Gemini extraction failed: {str(e)}"
        )

        print(
            "GEMINI ERROR:",
            str(e)
        )

        return None