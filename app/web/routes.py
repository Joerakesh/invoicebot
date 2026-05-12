from fastapi import (
    APIRouter,
    Request,
    UploadFile,
    File
)

from fastapi.responses import JSONResponse

from fastapi.templating import Jinja2Templates
import shutil
import os

from app.connectors.gmail import GmailConnector

from app.core.processor import process_invoice

router = APIRouter()

templates = Jinja2Templates(
    directory="app/web/templates"
)

PARSER_MODE = "offline"


@router.get("/")
def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "title": "InvoiceBot Dashboard"
        }
    )


@router.post("/parser/set")
async def set_parser(request: Request):

    global PARSER_MODE

    data = await request.json()

    mode = data.get("mode")

    PARSER_MODE = mode

    print(f"PARSER MODE CHANGED: {mode}")

    return JSONResponse(
        {
            "success": True,
            "message": f"Parser changed to {mode}"
        }
    )


@router.post("/gmail/fetch")
def gmail_fetch():

    try:

        connector = GmailConnector()

        files = connector.fetch()

        return JSONResponse(
            {
                "success": True,
                "message": f"{len(files)} Gmail invoices downloaded",
                "files": files
            }
        )

    except Exception as e:

        print("GMAIL ERROR:", str(e))

        return JSONResponse(
            {
                "success": False,
                "message": str(e)
            },
            status_code=500
        )


@router.get("/whatsapp/status")
def whatsapp_status():

    return JSONResponse(
        {
            "success": True,
            "status": "Webhook Active"
        }
    )


@router.post("/upload")
async def upload_invoice(
    file: UploadFile = File(...)
):

    try:

        os.makedirs(
            "storage/incoming",
            exist_ok=True
        )

        save_path = f"storage/incoming/{file.filename}"

        with open(save_path, "wb") as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

        print(f"LOCAL PDF SAVED: {save_path}")
        
        process_invoice(
            save_path,
            source="local"
        )

        return JSONResponse(
            {
                "success": True,
                "message": f"{file.filename} uploaded successfully"
            }
        )

    except Exception as e:

        print("UPLOAD ERROR:", str(e))

        return JSONResponse(
            {
                "success": False,
                "message": str(e)
            },
            status_code=500
        )


@router.get("/health")
def health():

    return JSONResponse(
        {
            "status": "running",
            "parser_mode": PARSER_MODE
        }
    )