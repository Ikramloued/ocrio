## Ocrio = OCR + Intelligence & Innovation
📄 PDF OCR & LLM Web App

Ocrio is a Flask + Dash web application that performs OCR on uploaded PDF files, enhances the extracted text using Ollama LLMs, and allows users to download the results in .txt and .docx formats. It also includes an embedded dashboard for visualization.

# 🚀 Features
Upload PDF files for processing
OCR extraction from scanned PDFs
Support for multi-page documents
Support for multilingual OCR (Arabic + Latin)
LLM-based text cleaning and structuring
Export results as .txt and .docx
Download processed files
Batch processing of multiple PDFs
Embedded Dash dashboard for visualization
Fully Dockerized application
🧠 LLM Options
Mode	Model
arabic	command-r7b-arabic:latest
latin	deepseek-r1:14b
multilingual	multilingual cleaning prompt
none	no LLM processing
#  Architecture
🔹 Frontend
Flask Templates (index.html)
Upload PDF
Select OCR language
Select LLM
Download results
Dash Dashboard (/dash/)
Visualize processed text
Analytics and charts
🔹 Backend
Flask Server
/ → Upload PDF
/process/<filename> → OCR + LLM processing
/process_folder → Batch processing
/processed/<filename> → Download files
Dash App
Embedded in Flask
Handles visualization
🔹 OCR Processing
ocr.ocr_processor.ocr_pdf(pdf_path, lang)
Converts PDF → images
Processes each page
Combines text
Supports:
fra
eng
ara
ara+fra+eng
🔹 LLM Processing
llm.llm_processor.process_with_llm(text, llm_type)
Cleans OCR errors
Structures paragraphs
Preserves original language
No hallucination / no added content
🔹 Output

Files saved in:

/processed/
.txt
.docx
📂 Project Structure
my_pdf_app/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── .dockerignore
│
├── dash_app/
│   ├── layout.py
│   └── callbacks.py
│
├── llm/
│   └── llm_processor.py
│
├── ocr/
│   └── ocr_processor.py
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── logo.png
│
├── uploads/
└── processed/
# 🔄 Workflow
User
│
│ Upload PDF + select language + LLM
▼
Flask '/'
│
├─ Save PDF → /uploads/
▼
Flask '/process'
│
├─ OCR
│   ├─ Split pages
│   ├─ OCR each page
│   └─ Combine text
│
├─ LLM (optional)
│   └─ Clean + structure text
│
├─ Save results
│   ├─ TXT
│   └─ DOCX
│
▼
Return download links + dashboard
# 🐳 Docker Usage
🔽 Pull from Docker Hub (recommended)
docker pull ikramloued/ocrio-app:latest
▶️ Run the container
docker run -p 5000:5000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ikramloued/ocrio-app:latest
🌐 Access the app
http://localhost:5000
🛠 Local Build (optional)
docker build -t ocrio-app .
docker run -p 5000:5000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ocrio-app
⚠️ Requirements
Docker installed
Ollama installed locally
Ollama running on:
http://localhost:11434

Test:

curl http://localhost:11434/api/tags
# 🧩 Notes
Ollama is not inside Docker

The container connects to Ollama via:

host.docker.internal
Supports:
multilingual documents
multi-page PDFs
batch processing
📊 Dashboard

Access:

http://localhost:5000/dash/
Text analytics
Visualization
Metrics
🧠 Summary

Ocrio is a complete OCR + LLM pipeline:

Extract text from scanned PDFs
Clean and structure with LLMs
Support multilingual documents
Export results
Visualize data
Run anywhere via Docker
👤 Author

Ikram Loued

⭐ Quick Start (1 command)
docker run -p 5000:5000 -e OLLAMA_BASE_URL=http://host.docker.internal:11434 ikramloued/ocrio-app:latest
