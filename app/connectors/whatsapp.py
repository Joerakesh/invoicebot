import os
import requests

from app.config.settings import settings


def download_whatsapp_media(media_id: str, filename: str):

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_ACCESS_TOKEN}"
    }

    # STEP 1 — Get media URL
    media_url_response = requests.get(
        f"https://graph.facebook.com/v22.0/{media_id}",
        headers=headers
    )

    media_data = media_url_response.json()

    print("MEDIA DATA:", media_data)

    download_url = media_data["url"]

    # STEP 2 — Download actual file
    file_response = requests.get(
        download_url,
        headers=headers
    )

    save_path = os.path.join(
        "storage/incoming",
        filename
    )

    with open(save_path, "wb") as f:
        f.write(file_response.content)

    print("WHATSAPP PDF SAVED:", save_path)

    return save_path