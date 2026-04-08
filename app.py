from flask import Flask, request, render_template, redirect, url_for, send_file
from dash import Dash
from werkzeug.utils import secure_filename
import os

from llm.llm_processor import process_with_llm
from ocr.ocr_processor import ocr_pdf, save_as_docx

# -------------------------------
# Configuration
# -------------------------------
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

server = Flask(__name__)
server.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
server.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# -------------------------------
# Dash app (embedded)
# -------------------------------
app = Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/'
)

from dash_app import layout, callbacks
app.layout = layout.get_layout()
callbacks.register_callbacks(app)


def normalize_ocr_lang(lang_value: str) -> str:
    """
    Mappe les valeurs du formulaire vers les langues Tesseract.
    """
    if lang_value == "multi":
        return "ara+fra+eng"
    return lang_value or "eng"


# -------------------------------
# OCR PDF UNIQUE
# -------------------------------
@server.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files.get('pdf_file')
        if not file or file.filename == '':
            return "Aucun fichier sélectionné"

        filename = secure_filename(file.filename)
        pdf_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(pdf_path)

        lang = request.form.get("lang", "eng")
        llm = request.form.get("llm", "none")

        return redirect(
            url_for('process_file', filename=filename, lang=lang, llm=llm)
        )

    return render_template('index.html')


# -------------------------------
# Traitement fichier unique
# -------------------------------
@server.route('/process/<filename>')
def process_file(filename):
    lang = request.args.get("lang", "eng")
    llm = request.args.get("llm", "none")

    tesseract_lang = normalize_ocr_lang(lang)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)

    raw_text = ocr_pdf(pdf_path, lang=tesseract_lang)

    final_text = raw_text if llm == "none" else process_with_llm(raw_text, llm)

    base = os.path.splitext(filename)[0]
    safe_llm = secure_filename(llm) or "none"

    txt_path = os.path.join(PROCESSED_FOLDER, f"{base}_{safe_llm}.txt")
    docx_path = os.path.join(PROCESSED_FOLDER, f"{base}_{safe_llm}.docx")

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    save_as_docx(final_text, docx_path)

    return f"""
        <h2>OCR terminé ✅</h2>
        <p>Langue OCR utilisée : <strong>{tesseract_lang}</strong></p>
        <p>TXT : <a href="/processed/{os.path.basename(txt_path)}">Télécharger</a></p>
        <p>DOCX : <a href="/processed/{os.path.basename(docx_path)}">Télécharger</a></p>
        <a href="/">⬅ Retour</a>
    """


# -------------------------------
# OCR BATCH DOSSIER
# -------------------------------
@server.route('/process_folder', methods=['POST'])
def process_folder():
    lang = request.form.get('lang', 'fra')
    llm = request.form.get('llm', 'none')

    tesseract_lang = normalize_ocr_lang(lang)
    uploaded_files = request.files.getlist('pdf_folder')

    if not uploaded_files:
        return "Aucun fichier reçu", 400

    first_path = uploaded_files[0].filename
    source_root = os.path.dirname(first_path)
    output_dir = os.path.join(source_root, "doc_ocr")
    os.makedirs(output_dir, exist_ok=True)

    for file in uploaded_files:
        if not file.filename.lower().endswith(".pdf"):
            continue

        filename = os.path.basename(file.filename)
        temp_pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        file.save(temp_pdf_path)

        text = ocr_pdf(temp_pdf_path, lang=tesseract_lang)
        final_text = text if llm == "none" else process_with_llm(text, llm)

        base = os.path.splitext(filename)[0]
        out_txt = os.path.join(output_dir, f"{base}_ocr.txt")

        with open(out_txt, "w", encoding="utf-8") as f:
            f.write(final_text)

    return render_template(
        "index.html",
        message=f"OCR batch terminé ✅ Résultats dans : {output_dir}"
    )


# -------------------------------
# Static serving
# -------------------------------
@server.route('/processed/<path:filename>')
def serve_processed(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), as_attachment=True)


# -------------------------------
# Run server
# -------------------------------
if __name__ == '__main__':
    server.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)