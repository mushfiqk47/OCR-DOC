<div align="center">

# DocIntel — Document Intelligence Platform

**An enterprise-grade, AI-powered toolkit for OCR, document conversion, table extraction, and translation — all running locally for complete data privacy.**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Next.js](https://img.shields.io/badge/Next.js-16-000000?logo=nextdotjs&logoColor=white)](https://nextjs.org)
[![Ollama](https://img.shields.io/badge/Ollama-Local_AI-white?logo=ollama&logoColor=black)](https://ollama.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## Table of Contents

- [Overview](#overview)
- [Features](#-features)
- [Complete Tool Catalog](#-complete-tool-catalog)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Install & Start Ollama](#1-install--start-ollama)
  - [2. Create the Custom AI Model](#2-create-the-custom-ai-model)
  - [3. Set Up the Backend](#3-set-up-the-backend)
  - [4. Set Up the Frontend](#4-set-up-the-frontend)
  - [Quick Start (Windows)](#quick-start-windows)
- [Configuration](#%EF%B8%8F-configuration)
- [API Reference](#-api-reference)
- [How It Works](#-how-it-works)
- [Supported Formats](#-supported-formats)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## Overview

DocIntel is a full-stack document intelligence platform that combines a **FastAPI** backend, a **Next.js** frontend, and a locally-hosted **Ollama** AI model to deliver 20+ document processing tools — all without sending your data to any cloud service.

Upload a scanned PDF, a photo of a receipt, or a spreadsheet screenshot, and DocIntel will extract text, parse tables, translate content, or convert between formats — right from your browser.

---

## 🚀 Features

| Feature | Description |
|---|---|
| **Pixel-Perfect OCR** | Extract text from images and PDFs with Markdown-formatted output (headers, lists, bold text). |
| **Intelligent Table Extraction** | Parse complex tables into structured Markdown, CSV, or Excel formats. |
| **Layout-Preserving Translation** | Translate entire documents while maintaining their original visual structure. |
| **20+ Conversion Tools** | Seamlessly convert between PDF, Word, Excel, CSV, HTML, JPG, and PNG. |
| **QR & Barcode Tools** | Generate QR codes from text and scan/decode QR codes and barcodes from images. |
| **Real-Time Streaming OCR** | Watch extracted text appear in real time via Server-Sent Events (SSE). |
| **Multi-Page Processing** | Process multi-page PDFs with concurrent page handling (up to 5 pages in parallel). |
| **100% Local & Private** | All AI inference runs locally through Ollama — your documents never leave your machine. |

---

## 🧰 Complete Tool Catalog

### Document Conversion
| Tool | Input | Output | Description |
|---|---|---|---|
| **PDF to Text** | PDF | Text | Extract raw text content from PDF files. |
| **PDF to Word** | PDF | DOCX | Convert PDF documents into editable Word files. |
| **PDF to HTML** | PDF | HTML | Convert PDF content to an HTML page. |
| **Word to PDF** | DOCX | PDF | Convert Word documents to PDF format. |
| **HTML to PDF** | HTML | PDF | Render HTML files as PDF documents. |
| **Text to PDF** | Text | PDF | Generate a PDF from plain text input. |
| **Text to Word** | Text | DOCX | Generate a Word document from plain text input. |
| **JPG to Word** | Image | DOCX | OCR an image and save the extracted text as a Word file. |

### Spreadsheet Tools
| Tool | Input | Output | Description |
|---|---|---|---|
| **PDF to Excel** | PDF | XLSX | Extract tables from all PDF pages into an Excel workbook. |
| **PDF to CSV** | PDF | CSV | Extract the first detected table from a PDF as a CSV file. |
| **JPG to Excel** | Image | XLSX | OCR a table from an image and export it to Excel. |
| **Excel to JPG** | XLSX | JPG | Render the first sheet of an Excel file as an image. |

### Image Tools
| Tool | Input | Output | Description |
|---|---|---|---|
| **PDF to JPG** | PDF | JPG | Render the first page of a PDF as a JPEG image. |
| **Word to JPG** | DOCX | JPG | Convert a Word document's first page to a JPEG image. |
| **Image to PDF** | Image(s) | PDF | Combine one or more images into a single PDF. |
| **Merge PDF** | PDFs | PDF | Merge multiple PDF files into one document. |
| **Invert Image** | Image | PNG | Invert the colors of an uploaded image. |
| **Text to Image** | Text | PNG | Render plain text as a PNG image. |
| **Image Translator** | Image | Text | OCR an image and translate its content to another language. |

### Scan & Code
| Tool | Input | Output | Description |
|---|---|---|---|
| **QR Generator** | Text | PNG | Create a QR code image from text or a URL. |
| **QR Scanner** | Image | Text | Decode QR code content from an uploaded image. |
| **Barcode Scanner** | Image | Text | Decode barcode data from an uploaded image. |

### Translation
| Tool | Input | Output | Description |
|---|---|---|---|
| **PDF Translator** | PDF | PDF | Translate an entire PDF while preserving its layout. |

---

## 🏗 Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      User's Browser                      │
│                   http://localhost:3000                   │
│                                                          │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐  │
│  │ FileUploader │  │ MarkdownView │  │    DataGrid    │  │
│  │  (Dropzone)  │  │   (Result)   │  │ (Table Result) │  │
│  └──────┬───────┘  └──────────────┘  └────────────────┘  │
│         │              Next.js 16 + React 19              │
└─────────┼────────────────────────────────────────────────┘
          │  HTTP / SSE
          ▼
┌──────────────────────────────────────────────────────────┐
│                   FastAPI Backend                         │
│                   http://localhost:8000                   │
│                                                          │
│  ┌────────────────────── Routers ──────────────────────┐ │
│  │  /api/ocr/*   /api/convert/*   /api/table/*         │ │
│  │  /api/translate/*              /health               │ │
│  └──────────────────────┬──────────────────────────────┘ │
│                         │                                │
│  ┌────────────── Service Layer ────────────────────────┐ │
│  │  ollama_client    pdf_service     image_service      │ │
│  │  table_parser     table_merger    excel_service      │ │
│  │  conversion_svc   office_service  barcode_service    │ │
│  │  translation_service                                 │ │
│  └──────────────────────┬──────────────────────────────┘ │
└─────────────────────────┼────────────────────────────────┘
                          │  HTTP (localhost:11434)
                          ▼
              ┌───────────────────────┐
              │     Ollama Server     │
              │    (Local AI Model)   │
              │                       │
              │  ┌─────────────────┐  │
              │  │  docintel model │  │
              │  │  (glm-ocr base) │  │
              │  └─────────────────┘  │
              └───────────────────────┘
```

**Request Flow:**
1. The user uploads a file or enters text through the **Next.js frontend**.
2. The frontend sends a `POST` request (with `FormData`) to the **FastAPI backend**.
3. The backend **router** validates the input and delegates to the appropriate **service**.
4. For OCR and translation tasks, the service preprocesses the image (resize, base64 encode) and sends it to the **Ollama** model.
5. Results are returned as downloadable files, JSON responses, or real-time SSE streams.

---

## 🛠 Tech Stack

### Backend (Python)
| Component | Technology | Purpose |
|---|---|---|
| Web Framework | [FastAPI](https://fastapi.tiangolo.com/) 0.115+ | Async REST API with auto-generated docs |
| Server | [Uvicorn](https://www.uvicorn.org/) | ASGI server for FastAPI |
| AI Integration | [Ollama](https://ollama.com/) via `httpx` | Local LLM inference (OCR, translation) |
| PDF Processing | `pypdfium2`, `pypdf`, `pdf2image` | Render, read, and merge PDFs |
| OCR Engine | `pytesseract` | Tesseract-based text recognition |
| Office Formats | `python-docx`, `openpyxl`, `reportlab` | Read/write Word & Excel, generate PDFs |
| Image Processing | `opencv-python-headless`, `Pillow` | Resize, preprocess, and encode images |
| Data Handling | `pandas` | Tabular data parsing and CSV/Excel export |
| QR / Barcode | `qrcode`, `pyzbar` | Generate and decode codes |
| Configuration | `pydantic-settings`, `python-dotenv` | Type-safe settings with `.env` support |

### Frontend (TypeScript)
| Component | Technology | Purpose |
|---|---|---|
| Framework | [Next.js 16](https://nextjs.org/) (React 19) | Server/client rendering with App Router |
| Styling | [Tailwind CSS v4](https://tailwindcss.com/) | Utility-first responsive design |
| Icons | [Lucide React](https://lucide.dev/) | Consistent icon set |
| Animations | [Framer Motion](https://www.framer.com/motion/) | Smooth UI transitions |
| File Uploads | [React Dropzone](https://react-dropzone.js.org/) | Drag-and-drop file input |
| Markdown | [React Markdown](https://remarkjs.github.io/react-markdown/) + `remark-gfm` | Render OCR results with formatting |
| Data Tables | [TanStack React Table](https://tanstack.com/table) | Display extracted table data |

### AI Model
| Component | Detail |
|---|---|
| Provider | Ollama (runs 100% locally) |
| Base Model | `glm-ocr` (GLM-4V, specialized for vision tasks) |
| Custom Model | `docintel` — extends `glm-ocr` with deterministic output (`temperature 0.0`), extended context window (8192 tokens), and a system prompt for structured extraction |

---

## 📂 Project Structure

```
OCR-DOC/
├── backend/                        # Python FastAPI application
│   ├── main.py                     # App entry point, middleware, router registration
│   ├── config.py                   # Settings (Ollama URL, model names, limits)
│   ├── requirements.txt            # Python dependencies
│   ├── routers/                    # API endpoint definitions
│   │   ├── ocr.py                  #   POST /api/ocr/text (streaming OCR)
│   │   ├── table.py                #   POST /api/ocr/table (table extraction)
│   │   ├── translate.py            #   POST /api/ocr/translate (translation)
│   │   └── conversion.py           #   POST /api/convert/* (20+ conversion endpoints)
│   ├── services/                   # Core business logic
│   │   ├── ollama_client.py        #   Ollama API wrapper (streaming & non-streaming)
│   │   ├── pdf_service.py          #   PDF-to-image rendering (pypdfium2)
│   │   ├── image_service.py        #   Image preprocessing & base64 encoding
│   │   ├── conversion_service.py   #   Format conversion utilities
│   │   ├── table_parser.py         #   Markdown table → pandas DataFrame
│   │   ├── table_merger.py         #   Multi-page table consolidation
│   │   ├── excel_service.py        #   DataFrame → Excel export
│   │   ├── office_service.py       #   Word/PDF interop
│   │   ├── barcode_service.py      #   QR/Barcode generation & decoding
│   │   └── translation_service.py  #   Layout-preserving PDF translation
│   └── schemas/                    # Pydantic request/response models
│       └── models.py
│
├── frontend/                       # Next.js TypeScript application
│   ├── package.json                # Node.js dependencies
│   ├── next.config.ts              # Next.js configuration
│   ├── tsconfig.json               # TypeScript compiler settings
│   └── src/
│       ├── app/
│       │   ├── layout.tsx          # Root layout (Shell wrapper)
│       │   ├── page.tsx            # Home page (tool catalog with search)
│       │   ├── globals.css         # Global Tailwind styles
│       │   └── [tool]/             # Dynamic route for each tool
│       │       └── page.tsx        # Universal tool page component
│       ├── components/
│       │   ├── Shell.tsx           # App layout wrapper
│       │   ├── Sidebar.tsx         # Navigation sidebar with categories
│       │   ├── FileUploader.tsx    # Drag-and-drop file upload component
│       │   ├── LanguageSelector.tsx# Language dropdown (100+ languages)
│       │   ├── MarkdownViewer.tsx  # Rendered Markdown output display
│       │   └── DataGrid.tsx        # TanStack table for structured data
│       └── constants/
│           └── languages.ts        # Supported language list
│
├── ollama/                         # AI model configuration
│   └── Modelfile                   # Custom model definition for Ollama
│
├── run.cmd                         # Windows quick-start script
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## ⚡ Getting Started

### Prerequisites

Before you begin, make sure you have the following installed on your system:

| Requirement | Version | Installation |
|---|---|---|
| **Python** | 3.10 or higher | [python.org/downloads](https://www.python.org/downloads/) |
| **Node.js** | v20 or higher | [nodejs.org](https://nodejs.org/) |
| **Ollama** | Latest | [ollama.com/download](https://ollama.com/download) |
| **Tesseract OCR** | Latest | See [Tesseract installation guide](#installing-tesseract-ocr) |

### 1. Install & Start Ollama

Download and install Ollama from [ollama.com/download](https://ollama.com/download), then make sure it is running:

```bash
ollama serve
```

> Ollama typically runs automatically after installation. You can verify it is running by visiting [http://localhost:11434](http://localhost:11434) in your browser.

### 2. Create the Custom AI Model

Pull the base model and create the custom DocIntel model:

```bash
# Navigate to the ollama directory
cd ollama

# Create the custom model from the Modelfile
ollama create docintel -f Modelfile
```

This creates a model called `docintel` based on `glm-ocr` with optimized settings for document analysis (zero temperature for deterministic output and an 8192-token context window).

### 3. Set Up the Backend

```bash
# Navigate to the backend directory
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv

# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The API server will start at **http://localhost:8000**.
Interactive API docs are available at **http://localhost:8000/docs**.

### 4. Set Up the Frontend

Open a **new terminal** and run:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the development server
npm run dev
```

The web interface will be available at **http://localhost:3000**.

### Quick Start (Windows)

On Windows you can start both services with a single command from the project root:

```cmd
run.cmd
```

This opens separate terminal windows for the backend and frontend.

---

## ⚙️ Configuration

All backend settings are managed through `backend/config.py` using [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/). Defaults work out of the box. To customize, create a `.env` file in the `backend/` directory:

```env
# Ollama connection
OLLAMA_BASE_URL=http://localhost:11434

# AI models
OCR_MODEL=docai-ocr
TRANSLATION_MODEL=translategemma:4b

# Processing settings
PDF_DPI=300
MAX_FILE_SIZE_MB=50
```

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | URL of the running Ollama instance. |
| `OCR_MODEL` | `docai-ocr` | Ollama model used for OCR and text extraction. |
| `TRANSLATION_MODEL` | `translategemma:4b` | Ollama model used for text translation. |
| `PDF_DPI` | `300` | DPI resolution for rendering PDF pages to images. Higher values improve accuracy but use more memory. |
| `MAX_FILE_SIZE_MB` | `50` | Maximum allowed upload file size in megabytes. |

### CORS Settings

The backend allows requests from these origins by default:

- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

To modify allowed origins, edit the `CORSMiddleware` configuration in `backend/main.py`.

---

## 📡 API Reference

All endpoints are documented interactively at **http://localhost:8000/docs** (Swagger UI) once the backend is running.

### Health Check

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Returns server status and the configured OCR model name. |

### OCR Endpoints (`/api/ocr`)

| Method | Endpoint | Input | Output | Description |
|---|---|---|---|---|
| `POST` | `/api/ocr/text` | Image or PDF file | SSE stream (JSON lines) | Streaming OCR — extracts text page by page in real time. |

### Table Endpoints (`/api/ocr`)

| Method | Endpoint | Input | Output | Description |
|---|---|---|---|---|
| `POST` | `/api/ocr/table` | Image or PDF file | JSON (table data + download ID) | Extracts tables and returns structured data. |
| `GET` | `/api/ocr/download/{file_id}` | File ID (from table extraction) | Excel file (.xlsx) | Download the extracted tables as an Excel workbook. |

### Translation Endpoints (`/api/ocr`)

| Method | Endpoint | Input | Output | Description |
|---|---|---|---|---|
| `POST` | `/api/ocr/translate` | Image/PDF file + `target_language` | JSON (original + translated text) | OCR and translate document content. |

### Conversion Endpoints (`/api/convert`)

| Method | Endpoint | Input | Output |
|---|---|---|---|
| `POST` | `/api/convert/text-to-pdf` | `text` (form field) | PDF file |
| `POST` | `/api/convert/pdf-to-text` | PDF file | JSON `{ "text": "..." }` |
| `POST` | `/api/convert/pdf-to-word` | PDF file | DOCX file |
| `POST` | `/api/convert/pdf-to-html` | PDF file | HTML file |
| `POST` | `/api/convert/pdf-to-jpg` | PDF file | JPEG image |
| `POST` | `/api/convert/pdf-to-excel` | PDF file | Excel file (.xlsx) |
| `POST` | `/api/convert/pdf-to-csv` | PDF file | CSV file |
| `POST` | `/api/convert/word-to-pdf` | DOCX file | PDF file |
| `POST` | `/api/convert/word-to-jpg` | DOCX file | JPEG image |
| `POST` | `/api/convert/html-to-pdf` | HTML file | PDF file |
| `POST` | `/api/convert/text-to-word` | `text` (form field) | DOCX file |
| `POST` | `/api/convert/jpg-to-word` | Image file | DOCX file |
| `POST` | `/api/convert/jpg-to-excel` | Image file | Excel file (.xlsx) |
| `POST` | `/api/convert/excel-to-jpg` | Excel file (.xlsx) | JPEG image |
| `POST` | `/api/convert/images-to-pdf` | Image file(s) | PDF file |
| `POST` | `/api/convert/merge-pdf` | PDF file(s) | Merged PDF file |
| `POST` | `/api/convert/invert-image` | Image file | PNG image (inverted) |
| `POST` | `/api/convert/text-to-image` | `text` (form field) | PNG image |
| `POST` | `/api/convert/image-translator` | Image file + `target_language` | JSON (original + translated text) |
| `POST` | `/api/convert/qr-generator` | `text` (form field) | PNG image (QR code) |
| `POST` | `/api/convert/qr-scanner` | Image file | JSON `{ "text": "..." }` |
| `POST` | `/api/convert/barcode-scanner` | Image file | JSON `{ "text": "..." }` |
| `POST` | `/api/convert/pdf-translator` | PDF file + `target_language` | Translated PDF file |

---

## 🔍 How It Works

### OCR Pipeline

```
Image/PDF  →  Preprocess (resize to max 2048px, convert to RGB)
           →  Base64 encode
           →  Send to Ollama with extraction prompt
           →  Receive Markdown-formatted text
           →  Stream to frontend via SSE
```

### Table Extraction Pipeline

```
Image/PDF  →  Render pages at 300 DPI
           →  OCR each page with table-specific prompt
           →  Parse Markdown tables with regex
           →  Convert to pandas DataFrames
           →  Merge split tables across pages (header matching)
           →  Export to Excel (.xlsx) with one sheet per table
```

### Translation Pipeline

```
Image/PDF  →  OCR to extract text (preserves Markdown)
           →  Translate text via translation model
           →  Convert translated Markdown to styled HTML
           →  Generate PDF with layout approximation
```

### Concurrency & Performance

- **Semaphore:** Limits concurrent Ollama requests to 5 for stability (hardcoded in `conversion_service.py` and `translation_service.py`).
- **Async I/O:** All network and file operations use Python's `asyncio`.
- **Threading:** CPU-bound tasks (e.g., DOCX→PDF) use `ThreadPoolExecutor`.
- **Temp File Cleanup:** Generated files auto-delete after download; orphaned files are cleaned at startup.

---

## 📋 Supported Formats

### Input Formats

| Format | Supported By |
|---|---|
| PDF | OCR, table extraction, translation, conversion |
| JPEG / PNG | OCR, table extraction, translation, inversion |
| DOCX (Word) | Conversion to PDF, JPG |
| XLSX (Excel) | Conversion to JPG |
| HTML | Conversion to PDF |
| Plain Text | Conversion to PDF, Word, Image |

### Output Formats

| Format | Generated By |
|---|---|
| PDF | Text-to-PDF, HTML-to-PDF, Word-to-PDF, Image-to-PDF, Merge, Translation |
| DOCX (Word) | Text-to-Word, JPG-to-Word, PDF-to-Word |
| XLSX (Excel) | PDF-to-Excel, JPG-to-Excel |
| CSV | PDF-to-CSV |
| HTML | PDF-to-HTML |
| JPEG / PNG | PDF-to-JPG, Word-to-JPG, Excel-to-JPG, Invert, Text-to-Image, QR Generator |
| Plain Text | PDF-to-Text, QR Scanner, Barcode Scanner |

---

## 🐛 Troubleshooting

### Ollama Connection Errors

**Symptom:** Backend returns `500` errors or "connection refused" messages.

**Solution:**
1. Verify Ollama is running: `ollama serve` or check [http://localhost:11434](http://localhost:11434).
2. Verify the model exists: `ollama list` — you should see `docintel` in the list.
3. If the model is missing, recreate it: `cd ollama && ollama create docintel -f Modelfile`.

### Tesseract Not Found

**Symptom:** `TesseractNotFoundError` when using OCR features.

<a id="installing-tesseract-ocr"></a>

**Solution — Install Tesseract:**
- **Windows:** Download the installer from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki) and add it to your `PATH`.
- **macOS:** `brew install tesseract`
- **Ubuntu / Debian:** `sudo apt install tesseract-ocr`

### Word-to-PDF Conversion Fails

**Symptom:** `500` error on the `/api/convert/word-to-pdf` endpoint.

**Solution:** This feature uses `docx2pdf`, which requires Microsoft Word on Windows or LibreOffice on Linux/macOS. Install LibreOffice if needed:
- **Ubuntu / Debian:** `sudo apt install libreoffice`
- **macOS:** `brew install --cask libreoffice`

### CORS Errors in Browser

**Symptom:** Browser console shows "Access-Control-Allow-Origin" errors.

**Solution:** Ensure your frontend is running on one of the allowed origins (`localhost:3000` or `localhost:3001`). To add custom origins, edit the CORS middleware in `backend/main.py`.

### File Upload Too Large

**Symptom:** `413` error when uploading a file.

**Solution:** The default limit is 50 MB. To increase it, set `MAX_FILE_SIZE_MB` in your `.env` file:

```env
MAX_FILE_SIZE_MB=100
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. **Fork** the repository.
2. **Create a branch** for your feature or fix: `git checkout -b feature/my-feature`.
3. **Make your changes** and test them locally.
4. **Submit a Pull Request** with a clear description of what you changed and why.

### Development Tips

- The backend has auto-reload enabled when run with `python main.py` — code changes take effect immediately.
- The frontend uses Next.js hot module replacement — UI changes appear instantly in the browser.
- Use **http://localhost:8000/docs** to test API endpoints interactively without the frontend.

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
