# DocIntel — Document Intelligence Platform

DocIntel is an enterprise-grade document intelligence solution designed for high-fidelity OCR, complex table extraction, and layout-preserving translation. It leverages a modern tech stack combining a high-performance FastAPI backend with a responsive Next.js frontend, powered by local AI models via Ollama.

## 🚀 Features

*   **Advanced OCR:** Extracts text with pixel-perfect accuracy, preserving formatting as Markdown (headers, lists).
*   **Intelligent Table Extraction:** robust parsing of complex tables into structured formats (Markdown, CSV, Excel).
*   **Layout-Preserving Translation:** Translates documents while maintaining their original visual structure.
*   **Multi-Format Conversion:** Seamlessly converts between PDF, DOCX, Images, and more.
*   **Barcode & QR Code:** Detection and decoding support.
*   **Local AI Privacy:** Fully local processing using Ollama and custom model definitions (`glm-ocr`), ensuring data privacy.

## 🛠️ Tech Stack

### Backend
*   **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
*   **Server:** Uvicorn
*   **Core Libraries:**
    *   `pypdfium2`, `pypdf`, `pdf2image` (PDF Processing)
    *   `pytesseract` (OCR Engine)
    *   `python-docx`, `openpyxl`, `reportlab` (Office Documents)
    *   `opencv-python-headless` (Image Processing)
    *   `pandas` (Data Analysis)
*   **AI Integration:** Ollama (Local LLM)

### Frontend
*   **Framework:** [Next.js 16](https://nextjs.org/) (React 19)
*   **Styling:** Tailwind CSS v4
*   **UI Components:** Lucide React (Icons), Framer Motion (Animations)
*   **State/Data:** React Query (implied via standard patterns), React Dropzone

### AI Model
*   **Provider:** Ollama
*   **Base Model:** Custom `glm-ocr` configuration
*   **Capabilities:** Structured extraction (Markdown text, Markdown tables, LaTeX formulas)

## 📂 Project Structure

```
├── backend/            # FastAPI Application
│   ├── routers/        # API Endpoints (OCR, Conversion, Table, Translate)
│   ├── services/       # Business Logic & File Processing Services
│   ├── schemas/        # Pydantic Models
│   ├── utils/          # Helper functions
│   ├── config.py       # Configuration settings
│   └── main.py         # App Entry Point
├── frontend/           # Next.js Application
│   ├── src/app/        # App Router Pages
│   ├── src/components/ # Reusable UI Components
│   └── ...
├── ollama/             # AI Model Configuration
│   └── Modelfile       # Custom Ollama Model Definition
└── ...
```

## ⚡ Getting Started

### Prerequisites
*   **Python:** 3.10+
*   **Node.js:** v20+
*   **Ollama:** Installed and running locally
*   **Tesseract OCR:** Installed on your system (required for `pytesseract`)

### 1. Model Setup (Ollama)
Ensure Ollama is installed, then create the custom model:
```bash
cd ollama
ollama create docintel -f Modelfile
```

### 2. Backend Setup
Navigate to the backend directory and set up the environment:

```bash
cd backend

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python main.py
# OR
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. API Docs at `http://localhost:8000/docs`.

### 3. Frontend Setup
Navigate to the frontend directory:

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```
The web interface will be available at `http://localhost:3000`.

## 📝 Configuration
*   **Backend:** Configuration is managed in `backend/config.py` and `.env` file (create one based on usage).
*   **Frontend:** `next.config.ts` handles Next.js settings.

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request.

## 📄 License
[MIT License](LICENSE)
