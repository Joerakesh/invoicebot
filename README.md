# InvoiceBot

Multi-source invoice automation platform built using Python, FastAPI, Docker, PostgreSQL, and WhatsApp Cloud API.

InvoiceBot automatically receives invoices from multiple sources, processes them, stores structured data, exports to Excel, and provides a live dashboard.

---

# Current Features

## Multi-Source Invoice Collection

Currently supported:

- WhatsApp Cloud API
- Gmail PDF Fetcher
- Local Upload

Planned:

- Outlook Integration
- OneDrive Integration

---

# WhatsApp Automation

- Real-time Meta webhook integration
- Automatic PDF detection
- Automatic media download
- Automatic invoice processing pipeline

---

# Gmail Integration

- OAuth Gmail authentication
- Automatically fetches unread PDF invoices
- Downloads attachments into processing pipeline

---

# Central Invoice Processing Engine

All invoice sources use one centralized processor.

Pipeline:

```text
WhatsApp / Gmail / Upload
            ↓
      process_invoice()
            ↓
      PDF Extraction
            ↓
      Invoice Parsing
            ↓
      Duplicate Detection
            ↓
      PostgreSQL Storage
            ↓
      Excel Export
```

---

# PostgreSQL Storage

Invoices are permanently stored inside PostgreSQL.

Stored fields:

- Company
- Invoice Number
- Date
- VAT
- Total
- Currency
- Source
- Confidence
- Filename
- Created Time

---

# Excel Export System

Exports invoices into:

```text
storage/exports/Invoices_Master.xlsx
```

Features:

- Separate Excel sheet per company
- Source tracking
- Confidence tracking
- Duplicate prevention

---

# Dashboard UI

FastAPI dashboard includes:

- Invoice upload
- Gmail fetch button
- WhatsApp webhook support
- Parser mode toggle
- Live logs
- Invoice table
- System status

---

# Duplicate Detection

Prevents duplicate invoice insertion using invoice number validation inside PostgreSQL.

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
         Invoice Parsing
                 ↓
        Duplicate Detection
                 ↓
           PostgreSQL
                 ↓
            Excel Export
                 ↓
             Dashboard
```

---

# Tech Stack

| Technology         | Purpose               |
| ------------------ | --------------------- |
| Python             | Backend               |
| FastAPI            | Web API + Dashboard   |
| PostgreSQL         | Invoice Database      |
| SQLAlchemy         | ORM                   |
| Docker             | Containerization      |
| OpenPyXL           | Excel Export          |
| pdfplumber         | PDF Parsing           |
| Gmail API          | Email Integration     |
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
 ├── database/
 ├── models/
 ├── services/
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

# Run With Docker

```bash
docker compose up --build
```

---

# Initialize Database

```bash
docker compose exec invoicebot python -m app.init_db
```

---

# Start ngrok

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

---

# WhatsApp Webhook Setup

Inside Meta Developer Dashboard:

- Configure webhook URL
- Add verify token
- Subscribe to `messages`

---

# Gmail OAuth Setup

1. Create Google Cloud OAuth credentials
2. Download `credentials.json`
3. Place inside project root
4. Run Gmail connector once

```bash
python app/connectors/gmail.py
```

---

# Run Dashboard

Open:

```text
http://localhost:8000
```

---

# Current System Status

Implemented:

- WhatsApp invoice automation
- Gmail invoice fetching
- PostgreSQL storage
- Dashboard UI
- Company-wise Excel export
- Duplicate detection
- Source tracking
- Docker infrastructure

---

# Planned Improvements

- Outlook connector
- OneDrive connector
- Better offline invoice parser
- OCR support
- Background workers
- Cloud deployment
- Analytics dashboard
- Google Sheets sync
