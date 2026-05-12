import re


def clean_invoice_text(text: str):

    lines = text.splitlines()

    cleaned = []

    stop_keywords = [
        "terms & conditions",
        "customer support",
        "fssai",
        "otp",
        "reverse charge",
        "authorised signatory",
        "bank account details"
    ]

    for line in lines:

        line_lower = line.lower()

        if any(
            keyword in line_lower
            for keyword in stop_keywords
        ):
            continue

        # remove very long noisy lines
        if len(line) > 250:
            continue

        cleaned.append(line.strip())

    cleaned_text = "\n".join(cleaned)

    # remove excessive empty lines
    cleaned_text = re.sub(
        r"\n+",
        "\n",
        cleaned_text
    )

    return cleaned_text[:2000]