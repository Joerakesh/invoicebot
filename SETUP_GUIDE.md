# InvoiceBot API Setup Guide

This document explains how to get all required APIs and credentials for InvoiceBot.

Currently required:

- Gemini API Key
- Gmail OAuth Credentials
- WhatsApp Cloud API Credentials
- ngrok URL

---

# 1. Gemini API Setup

Gemini AI is used for invoice extraction.

InvoiceBot uses Gemini to identify:

- Company name
- Invoice number
- Total amount
- Currency
- VAT/GST
- Invoice date

---

## Step 1 — Open Google AI Studio

Open:

```text id="18n72k"
https://aistudio.google.com/app/apikey
```

---

## Step 2 — Sign In

Login using your Google account.

---

## Step 3 — Create API Key

Click:

```text id="5f6q8f"
Create API Key
```

Select:

```text id="u29mx6"
Create API key in new project
```

---

## Step 4 — Copy API Key

Example:

```text id="6kkx5t"
AIzaSyAxxxxxxxxxxxxxxxxxxxx
```

---

## Step 5 — Add To `.env`

```env id="j02sxf"
GEMINI_API_KEY=AIzaSyAxxxxxxxxxxxxxxxxxxxx
```

---

# 2. Gmail API Setup

InvoiceBot fetches unread invoice emails using Gmail API.

---

# Requirements

You need:

- Google Cloud Project
- Gmail API Enabled
- OAuth Consent Screen
- OAuth Client ID
- credentials.json file

---

## Step 1 — Open Google Cloud Console

Open:

```text id="r9rqzu"
https://console.cloud.google.com/
```

---

## Step 2 — Create Project

Top navigation bar:

```text id="h6fcjlwm"
Select Project → New Project
```

Project Name:

```text id="5jjlwm"
InvoiceBot
```

Click:

```text id="4xjlwm"
Create
```

---

## Step 3 — Enable Gmail API

Inside Google Cloud Console:

```text id="9qjlwm"
APIs & Services → Library
```

Search:

```text id="7rjlwm"
Gmail API
```

Click:

```text id="8mjlwm"
Enable
```

---

## Step 4 — Configure OAuth Consent Screen

Open:

```text id="3yjlwm"
APIs & Services → OAuth Consent Screen
```

Choose:

```text id="1jjlwm"
External
```

Click:

```text id="2hjlwm"
Create
```

---

## Step 5 — Fill App Details

Fill:

| Field              | Value      |
| ------------------ | ---------- |
| App Name           | InvoiceBot |
| User Support Email | Your Gmail |
| Developer Contact  | Your Gmail |

Save and Continue.

---

## Step 6 — Add Test User

Inside:

```text id="0njlwm"
Audience → Test Users
```

Click:

```text id="m4jlwm"
Add Users
```

Add your Gmail address.

Example:

```text id="6ujlwm"
example@gmail.com
```

Save.

IMPORTANT:

Without adding yourself as test user:

```text id="k1jlwm"
Error 403: access_denied
```

will happen.

---

## Step 7 — Create OAuth Client ID

Open:

```text id="p9jlwm"
APIs & Services → Credentials
```

Click:

```text id="q3jlwm"
Create Credentials
```

Choose:

```text id="a8jlwm"
OAuth Client ID
```

---

## Step 8 — Select Application Type

Choose:

```text id="f2jlwm"
Desktop App
```

Name:

```text id="g5jlwm"
InvoiceBot
```

Click:

```text id="r6jlwm"
Create
```

---

## Step 9 — Download Credentials

Download JSON file.

Rename it:

```text id="x7jlwm"
credentials.json
```

Place it in project root:

```text id="y9jlwm"
invoicebot/
 ├── credentials.json
 ├── docker-compose.yml
 └── app/
```

---

# Gmail OAuth Flow

When user clicks:

```text id="t1jlwm"
Connect Gmail
```

InvoiceBot:

1. Opens Google OAuth screen
2. User grants Gmail permission
3. OAuth token is generated
4. Token automatically saves to:

```text id="s3jlwm"
storage/token.json
```

This token is later used to:

- Read emails
- Download PDF attachments
- Mark emails as read

---

# Required Gmail Scope

InvoiceBot uses:

```text id="d4jlwm"
https://www.googleapis.com/auth/gmail.modify
```

This allows:

- Reading emails
- Downloading attachments
- Marking emails as read

---

# 3. WhatsApp Cloud API Setup

InvoiceBot supports invoice automation from WhatsApp.

---

## Step 1 — Open Meta Developers

Open:

```text id="w8jlwm"
https://developers.facebook.com/
```

Login using Facebook account.

---

## Step 2 — Create App

Click:

```text id="c5jlwm"
Create App
```

Choose:

```text id="z6jlwm"
Business
```

---

## Step 3 — Add WhatsApp Product

Inside dashboard:

```text id="n7jlwm"
Add Product → WhatsApp
```

---

## Step 4 — Get Credentials

Inside WhatsApp API setup page copy:

- Temporary Access Token
- Phone Number ID

---

## Step 5 — Add To `.env`

```env id="b2jlwm"
WHATSAPP_ACCESS_TOKEN=

WHATSAPP_PHONE_ID=
```

---

# 4. ngrok Setup

ngrok exposes local FastAPI server to internet.

Needed for:

- WhatsApp webhooks

---

## Step 1 — Download ngrok

Open:

```text id="l3jlwm"
https://ngrok.com/download
```

Install ngrok.

---

## Step 2 — Create ngrok Account

Create free account.

---

## Step 3 — Get Auth Token

Inside ngrok dashboard:

```text id="h4jlwm"
Your Authtoken
```

---

## Step 4 — Configure ngrok

Run:

```bash id="u5jlwm"
ngrok config add-authtoken YOUR_TOKEN
```

---

## Step 5 — Start Tunnel

Run:

```bash id="e6jlwm"
ngrok http 8000
```

Example:

```text id="v7jlwm"
https://abcd.ngrok-free.app
```

---

# 5. WhatsApp Webhook Setup

Webhook URL:

```text id="j8jlwm"
https://abcd.ngrok-free.app/webhook
```

Verify Token:

```text id="k9jlwm"
invoicebot123
```

Subscribe to:

```text id="m0jlwm"
messages
```

---

# Final Required Files

Project root should contain:

```text id="o1jlwm"
invoicebot/
 ├── credentials.json
 ├── .env
 ├── docker-compose.yml
 ├── run.sh
 └── app/
```

---

# Final Environment Variables

```env id="p2jlwm"
GEMINI_API_KEY=

GEMINI_MODEL=gemini-2.5-flash

WHATSAPP_ACCESS_TOKEN=

WHATSAPP_PHONE_ID=

VERIFY_TOKEN=invoicebot123
```

---

# Start InvoiceBot

```bash id="r3jlwm"
./run.sh
```

Dashboard:

```text id="s4jlwm"
http://localhost:8000
```
