import json
import re

from google import genai

from app.config.settings import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


def fallback_parser(text: str):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    company = "Unknown Company"
    invoice_no = "UNKNOWN"
    date = ""
    total = 0
    vat = 0

    # COMPANY

    for line in lines[:20]:

        upper = line.upper()

        if (
            "PRIVATE LIMITED" in upper
            or "LTD" in upper
            or "FOODS" in upper
            or "STORE" in upper
        ):

            company = line
            break

    # INVOICE NUMBER

    invoice_patterns = [

        r"Invoice Number\s*[:\-]?\s*([A-Z0-9\-]+)",
        r"Invoice No\s*[:\-]?\s*([A-Z0-9\-]+)",
        r"Invoice#\s*[:\-]?\s*([A-Z0-9\-]+)",

    ]

    for pattern in invoice_patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:

            candidate = match.group(1).strip()

            if len(candidate) < 25:

                invoice_no = candidate

                break

    # DATE

    date_pattern = re.search(
        r"(\d{1,2}[-/](?:\d{1,2}|[A-Za-z]{3})[-/]\d{2,4})",
        text
    )

    if date_pattern:

        date = date_pattern.group(1)

    # TOTAL

    totals = []

    for line in lines:

        if "total" in line.lower():

            numbers = re.findall(
                r"(\d+\.\d{2})",
                line
            )

            for n in numbers:

                try:
                    totals.append(float(n))
                except:
                    pass

    if not totals:

        all_numbers = re.findall(
            r"(\d+\.\d{2})",
            text
        )

        totals = [
            float(n)
            for n in all_numbers
            if float(n) > 100
        ]

    if totals:

        total = max(totals)

    vat = round(total * 0.05, 2)

    return {
        "company": company,
        "invoice_no": invoice_no,
        "date": date,
        "currency": "INR",
        "vat": vat,
        "total": total,
    }

def extract_invoice(text: str):

    try:

        short_text = text[:3500]

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
  "total": 0
}}

Rules:
- Extract seller company name only
- Ignore GST numbers
- Ignore PAN numbers
- Ignore CIN numbers
- invoice_no must be actual invoice number
- total must be final payable amount
- currency must be detected properly


Invoice Text:
{short_text}
"""

        print("CALLING GEMINI")

        response = client.models.generate_content(
            model=settings.GEMINI_MODEL,
            contents=prompt
        )

        print("GEMINI RESPONSE RECEIVED")

        content = response.text.strip()

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
        )

        data = json.loads(content)

        if not data.get("invoice_no"):
            data["invoice_no"] = "UNKNOWN"

        if not data.get("company"):
            data["company"] = "Unknown Company"

        print("AI EXTRACTION SUCCESS")

        return data

    except Exception as e:

        print("AI FAILED:", str(e))

        print("USING FALLBACK PARSER")

        return fallback_parser(text)