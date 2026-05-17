import os
import base64

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


class GmailConnector:

    def __init__(self):

        self.authenticate()

    def authenticate(self):

        token_path = "storage/token.json"

        self.creds = Credentials.from_authorized_user_file(
            token_path,
            SCOPES
        )

        self.service = build(
            "gmail",
            "v1",
            credentials=self.creds
        )

    def fetch(self):

        query = "is:unread has:attachment invoice"

        results = self.service.users().messages().list(
            userId="me",
            q=query,
            maxResults=20
        ).execute()

        messages = results.get("messages", [])

        downloaded_files = []

        os.makedirs(
            "storage/incoming",
            exist_ok=True
        )

        print("GMAIL MESSAGES FOUND:", len(messages))

        for msg in messages:

            msg_data = self.service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            payload = msg_data.get("payload", {})

            headers = payload.get("headers", [])

            subject = ""

            for h in headers:

                if h["name"] == "Subject":

                    subject = h["value"]

            print("EMAIL SUBJECT:", subject)

            parts = payload.get("parts", [])

            for part in parts:

                filename = part.get("filename")

                if filename and filename.lower().endswith(".pdf"):

                    attachment_id = part["body"]["attachmentId"]

                    attachment = self.service.users().messages().attachments().get(
                        userId="me",
                        messageId=msg["id"],
                        id=attachment_id
                    ).execute()

                    file_data = base64.urlsafe_b64decode(
                        attachment["data"]
                    )

                    save_path = f"storage/incoming/{filename}"

                    with open(save_path, "wb") as f:

                        f.write(file_data)

                    downloaded_files.append(save_path)

                    print("GMAIL PDF SAVED:", save_path)

            # MARK EMAIL AS READ

            self.service.users().messages().modify(
                userId="me",
                id=msg["id"],
                body={
                    "removeLabelIds": ["UNREAD"]
                }
            ).execute()

        return downloaded_files