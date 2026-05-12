import re


def extract_invoice(text: str):

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

            # avoid GSTIN confusion
            if len(candidate) < 25:

                invoice_no = candidate
                break
    # DATE
    date_pattern = re.search(
        r"(\\d{1,2}[-/](?:\\d{1,2}|[A-Za-z]{3})[-/]\\d{2,4})",
        text
    )

    if date_pattern:
        date = date_pattern.group(1)

    # TOTAL DETECTION
    totals = []

    for line in lines:

        if "total" in line.lower():

            numbers = re.findall(
                r"(\\d+\\.\\d{2})",
                line
            )

            for n in numbers:

                try:
                    totals.append(float(n))
                except:
                    pass

    # fallback
    if not totals:

        all_numbers = re.findall(
            r"(\\d+\\.\\d{2})",
            text
        )

        totals = [
            float(n)
            for n in all_numbers
            if float(n) > 100
        ]

    if totals:
        total = max(totals)

    # VAT
    vat = round(total * 0.05, 2)

    return {
        "company": company,
        "invoice_no": invoice_no,
        "date": date,
        "currency": "INR",
        "vat": vat,
        "total": total,
        "confidence": 0.90
    }