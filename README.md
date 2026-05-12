# InvoiceBot

AI-powered WhatsApp invoice automation system built using Python, FastAPI, Docker, and Google Gemini AI.

InvoiceBot automatically:

- Receives invoice PDFs from WhatsApp
- Downloads media files automatically
- Extracts invoice text from PDFs
- Cleans invoice noise
- Uses AI to extract structured invoice details
- Detects duplicate invoices
- Exports invoice data into Excel
- Organizes processed files

---

# Features

## WhatsApp Cloud API Integration

- Real-time webhook integration
- Automatic PDF detection
- Automatic media download

## AI Invoice Extraction

Uses Google Gemini AI to extract:

- Company name
- Invoice number
- Invoice date
- VAT/GST amount
- Total amount
- Currency
- Confidence score

## Duplicate Detection

Prevents duplicate invoice insertion using invoice number validation.

## Dockerized Infrastructure

Production-ready containerized backend using Docker Compose.

## File Lifecycle Management

Automatically manages:

- incoming invoices
- processed invoices
- failed invoices

---

# Architecture

```text
WhatsApp PDF
      ↓
Meta Webhook
      ↓
FastAPI Webhook Server
      ↓
Media Download
      ↓
PDF Extraction
      ↓
Invoice Cleaning
      ↓
Gemini AI Extraction
      ↓
Structured JSON
      ↓
Excel Export
      ↓
Duplicate Detection
      ↓
Processed Storage
```

---

# Tech Stack

| Technology         | Purpose                 |
| ------------------ | ----------------------- |
| Python             | Backend                 |
| FastAPI            | Webhook server          |
| Docker             | Containerization        |
| Gemini AI          | AI extraction           |
| pdfplumber         | PDF parsing             |
| OpenPyXL           | Excel export            |
| ngrok              | Local webhook tunneling |
| WhatsApp Cloud API | Real-time messaging     |

---

# Project Structure

```text
app/
 ├── ai/
 ├── config/
 ├── connectors/
 ├── core/
 ├── database/
 ├── models/
 ├── services/
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

# Start ngrok

```bash
ngrok http 8000
```

Copy generated URL.

Example:

```text
https://abcd.ngrok-free.app
```

Webhook URL:

```text
https://abcd.ngrok-free.app/webhook
```

---

# Meta Webhook Setup

Inside Meta Developer Dashboard:

- Configure webhook URL
- Add verify token
- Subscribe to `messages`

---

# Example Invoice Output

| Invoice No       | Company        | Date        | Total  |
| ---------------- | -------------- | ----------- | ------ |
| C145246T25102166 | Blink Commerce | 16-Nov-2025 | 213.00 |

---

# Future Improvements

- PostgreSQL integration
- Google Sheets sync
- Gmail automation
- OCR support
- Analytics dashboard
- Background workers
- Cloud deployment

---
