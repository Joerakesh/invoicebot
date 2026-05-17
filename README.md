# InvoiceBot

Multi-source invoice automation platform built using Python, FastAPI, Docker, Gmail API, WhatsApp Cloud API, and AI-powered invoice parsing.

InvoiceBot automatically receives invoice PDFs from multiple sources, extracts structured invoice data, exports invoices into Excel sheets, and provides a lightweight dashboard UI.

---

# Current Features

## Multi-Source Invoice Collection

Currently supported:

- Gmail Invoice Fetching
- WhatsApp Cloud API
- Local PDF Upload

Planned:

- Outlook Integration
- OneDrive Integration
- Google Drive Sync

---

# Gmail Invoice Automation

- OAuth Gmail authentication
- Automatically fetches unread invoice emails
- Detects PDF attachments
- Downloads invoices automatically
- Marks processed emails as read

---

# WhatsApp Invoice Automation

- Real-time Meta webhook integration
- Automatic PDF detection
- Automatic media download
- Automatic invoice processing

---

# Central Invoice Processing Pipeline

All invoice sources use one centralized processor.

Pipeline:

```text
WhatsApp / Gmail / Upload
            ↓
      process_invoice()
            ↓
        PDF Extraction
            ↓
       AI Invoice Parsing
            ↓
      Duplicate Detection
            ↓
         Excel Export
            ↓
       Processed Storage
```

---

# AI Invoice Extraction

InvoiceBot uses Gemini AI to extract:

- Company Name
- Invoice Number
- Invoice Date
- VAT / GST
- Total Amount
- Currency

Includes fallback offline parser if AI becomes unavailable.

---

# Excel Export System

Exports invoices into:

```text
storage/exports/Invoices_Master.xlsx
```

Features:

- Separate Excel sheet per company
- Source tracking
- Duplicate prevention
- Automatic workbook creation

Example sheets:

```text
Amazon
Blinkit
Swiggy
AR South Indian Foods
```

---

# Dashboard UI

FastAPI dashboard includes:

- Gmail OAuth login
- Fetch invoices button
- Local invoice upload
- System logs
- Gmail connection status
- Downloaded invoice list

---

# Duplicate Detection

Prevents duplicate invoice insertion using invoice number validation inside Excel sheets.

---

# File Lifecycle Management

Automatically manages:

- incoming invoices
- processed invoices
- failed invoices
- exported invoices

---

# Architecture

```text
            WhatsApp
                 ↓
              Webhook
                 ↓

 Gmail → process_invoice() ← Upload
                 ↓
          PDF Extraction
                 ↓
         AI Invoice Parsing
                 ↓
        Duplicate Detection
                 ↓
            Excel Export
                 ↓
          Processed Files
                 ↓
             Dashboard
```

---

# Tech Stack

| Technology         | Purpose               |
| ------------------ | --------------------- |
| Python             | Backend               |
| FastAPI            | API + Dashboard       |
| Docker             | Containerization      |
| Gemini AI          | Invoice Parsing       |
| Gmail API          | Email Integration     |
| OpenPyXL           | Excel Export          |
| pdfplumber         | PDF Parsing           |
| WhatsApp Cloud API | Messaging Integration |
| ngrok              | Webhook Tunneling     |

---

# Project Structure

```text
app/
 ├── ai/
 ├── config/
 ├── connectors/
 │    ├── gmail.py
 │    └── whatsapp.py
 ├── core/
 │    └── processor.py
 ├── services/
 │    └── excel_service.py
 ├── web/
 │    ├── routes.py
 │    └── templates/
 └── utils/

storage/
 ├── incoming/
 ├── processed/
 ├── failed/
 └── exports/
```

---

# Setup

## Clone Repository

```bash
git clone https://github.com/Joerakesh/invoicebot.git

cd invoicebot
```

---

# Environment Variables

Create `.env`

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_ID=

VERIFY_TOKEN=invoicebot123
```

---

# Gmail OAuth Setup

1. Create Google Cloud OAuth credentials
2. Download `credentials.json`
3. Place it in project root

Example:

```text
invoicebot/
 ├── credentials.json
 ├── docker-compose.yml
 └── app/
```

---

# Run InvoiceBot

## Option 1 — Docker

```bash
docker compose up --build
```

---

## Option 2 — One Click Startup

```bash
./run.sh
```

This automatically:

- Starts Docker containers
- Builds the project
- Opens dashboard in browser
- Streams logs

---

# Open Dashboard

```text
http://localhost:8000
```

---

# Gmail Login

Open dashboard and click:

```text
Connect Gmail
```

This stores OAuth token automatically inside:

```text
storage/token.json
```

---

# Fetch Gmail Invoices

Click:

```text
Fetch Invoices
```

InvoiceBot will:

- Search unread emails
- Detect invoice PDFs
- Download attachments
- Parse invoices
- Export to Excel
- Move processed files

---

# WhatsApp Webhook Setup

Start ngrok:

```bash
ngrok http 8000
```

Example:

```text
https://abcd.ngrok-free.app
```

Webhook URL:

```text
https://abcd.ngrok-free.app/webhook
```

Inside Meta Developer Dashboard:

- Configure webhook URL
- Add verify token
- Subscribe to `messages`

---

# Current System Status

Implemented:

- Gmail invoice fetching
- WhatsApp invoice automation
- AI invoice extraction
- Offline fallback parser
- Company-wise Excel export
- Duplicate detection
- Dashboard UI
- Docker infrastructure
- One-click startup script

---

# Planned Improvements

- Outlook connector
- OneDrive connector
- OCR support
- Background workers
- Google Sheets sync
- Analytics dashboard
- Cloud deployment
- Electron desktop app
- Automatic Gmail polling every 10 minutes
