from fastapi import FastAPI, Request

from app.connectors.whatsapp import download_whatsapp_media

from app.core.processor import process_invoice

from app.web.routes import router as web_router


app = FastAPI()

app.include_router(web_router)

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

    return {
        "error": "Invalid verification"
    }


@app.post("/webhook")
async def whatsapp_webhook(request: Request):

    body = await request.json()

    print("WHATSAPP WEBHOOK RECEIVED")

    print(body)

    try:

        changes = body["entry"][0]["changes"][0]["value"]

        if "messages" not in changes:

            return {
                "status": "no messages"
            }

        msg = changes["messages"][0]

        if msg["type"] != "document":

            return {
                "status": "not document"
            }

        document = msg["document"]

        media_id = document["id"]

        filename = document["filename"]

        saved_path = download_whatsapp_media(
            media_id,
            filename
        )

        if not saved_path:

            print("MEDIA DOWNLOAD FAILED")

            return {
                "status": "download failed"
            }

        process_invoice(
            saved_path,
            source="whatsapp"
        )

    except Exception as e:

        print("WEBHOOK ERROR:", str(e))

    return {
        "status": "received"
    }