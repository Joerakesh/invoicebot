import os
import base64

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from app.core.processor import process_invoice

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]


class GmailConnector:

    def __init__(self):

        self.service = self.authenticate()

    def authenticate(self):

        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file(
                "token.json",
                SCOPES
            )

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:

                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json",
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return build("gmail", "v1", credentials=creds)

    def fetch(self):

        results = self.service.users().messages().list(
            userId="me",
            q="has:attachment filename:pdf is:unread",
            maxResults=10
        ).execute()

        messages = results.get("messages", [])

        downloaded_files = []

        for msg in messages:

            msg_data = self.service.users().messages().get(
                userId="me",
                id=msg["id"]
            ).execute()

            payload = msg_data["payload"]

            parts = payload.get("parts", [])

            for part in parts:

                filename = part.get("filename")

                if filename.endswith(".pdf"):

                    attachment_id = part["body"]["attachmentId"]

                    attachment = self.service.users().messages().attachments().get(
                        userId="me",
                        messageId=msg["id"],
                        id=attachment_id
                    ).execute()

                    data = attachment["data"]

                    file_data = base64.urlsafe_b64decode(data)

                    save_path = f"storage/incoming/{filename}"

                    with open(save_path, "wb") as f:
                        f.write(file_data)

                    print("GMAIL PDF SAVED:", save_path)
                    
                    process_invoice(
                        save_path,
                        source="email"
                    )

                    downloaded_files.append(save_path)
                    
                    self.service.users().messages().modify(
                        userId='me',
                        id=msg["id"],
                        body={
                            'removeLabelIds': ['UNREAD']
                        }
                    ).execute()

        return downloaded_files


if __name__ == "__main__":

    connector = GmailConnector()

    connector.fetch()