from fastapi import FastAPI, Request
from app.connectors.whatsapp import download_whatsapp_media
from app.utils.pdf_reader import read_pdf
from app.utils.invoice_cleaner import clean_invoice_text
from app.ai.extractor import extract_invoice
from app.services.excel_service import save_invoice
from app.utils.file_handler import move_processed
app = FastAPI()

VERIFY_TOKEN = "invoicebot123"


@app.get("/webhook")
async def verify_webhook(request: Request):

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token:

        if token == VERIFY_TOKEN:
            return int(challenge)

    return {"error": "Invalid verification"}


@app.post("/webhook")
async def whatsapp_webhook(request: Request):

    body = await request.json()

    print("WHATSAPP WEBHOOK RECEIVED")
    print(body)

    try:

        changes = body["entry"][0]["changes"][0]["value"]

        if "messages" in changes:

            msg = changes["messages"][0]

            if msg["type"] == "document":

                document = msg["document"]

                media_id = document["id"]

                filename = document["filename"]

                download_whatsapp_media(
                    media_id,
                    filename
                )
                
                saved_path = download_whatsapp_media(
                    media_id,
                    filename
                )

                print("STARTING AI PROCESSING")

                text = read_pdf(saved_path)

                cleaned_text = clean_invoice_text(text)

                data = extract_invoice(cleaned_text)

                print("AI RESPONSE:", data)

                if data:

                    saved = save_invoice(data)

                    if saved:
                        print("EXCEL UPDATED")
                    else:
                        print("DUPLICATE DETECTED")

                    move_processed(saved_path)

                    print("FILE MOVED")

    except Exception as e:

        print("WEBHOOK ERROR:", str(e))

    return {"status": "received"}