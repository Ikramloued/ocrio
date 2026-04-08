
Ocrio = OCR + intelligence & innovation

# PDF OCR & LLM Web App

A Flask + Dash web application that performs OCR on uploaded PDF files, cleans the text using Ollama LLMs, and allows downloading the results in `.txt` and `.docx` formats. Users can also visualize processed data through an embedded Dash dashboard.

---

## **Features**

- Upload PDF files for processing
- Choose LLM type:
  - `arabic` → `command-r7b-arabic:latest`
  - `latin` → `deepseek-r1:14b`
  - `none` → skip LLM processing
- OCR extraction using `ocr_pdf`
- LLM text cleaning and formatting
- Save results as `.txt` and `.docx`
- Download processed files
- Embedded Dash dashboard for visualization

---

## **Architecture**

### **1️⃣ Frontend**
- Flask Templates (`index.html`)
  - Upload PDF file
  - Choose LLM type
  - Download links after processing
- Dash Dashboard (`/dash/`)
  - Display text statistics, charts, and analytics

### **2️⃣ Backend**
- Flask Server
  - `/` → Upload PDF
  - `/process/<filename>` → OCR + LLM processing + TXT/DOCX creation
  - `/download` → Serve processed files for download
- Dash App
  - Embedded inside Flask
  - Handles visualization and callbacks

### **3️⃣ OCR Processing**
- `ocr.ocr_processor.ocr_pdf(pdf_path, output_txt_path)`
  - Extracts text from PDF
  - Saves intermediate `.txt` file

### **4️⃣ LLM Processing**
- `llm.llm_processor.process_with_llm(raw_text, llm_type)`
  - Uses Ollama models:
    - Arabic → `command-r7b-arabic:latest`
    - Latin → `deepseek-r1:14b`
  - Returns cleaned/improved text

### **5️⃣ File Output**
- Results stored in `processed/`:
  - `.txt` → plain text
  - `.docx` → formatted document
- Download via Flask `send_file`

---

## **Folder Structure**

my_pdf_app/
│
├── app.py # Flask server + route handling
├── dash_app/
│ ├── layout.py # Dash layout
│ └── callbacks.py # Dash callbacks
├── llm/
│ └── llm_processor.py # LLM processing functions
├── ocr/
│ └── ocr_processor.py # OCR processing functions
├── templates/
│ └── index.html # File upload page
├── uploads/ # Temporary uploaded PDFs
└── processed/ # OCR/LLM outputs (.txt, .docx)

## **workflow diagram**
User
│
│ Upload PDF + choose LLM
▼
Flask Route: '/'
│
├─ Save PDF → /uploads/
▼
Flask Route: '/process/<filename>'
│
├─ OCR Processor → raw text → /processed/.txt
│
├─ LLM Processor → final text → /processed/.txt & .docx
│
▼
Return page with:

Download TXT

Download DOCX

Link to Dash Dashboard
│
▼
Dash App: '/dash/'
│
└─ Visualize / Analyze processed text