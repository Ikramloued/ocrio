from pdf2image import convert_from_path
import pytesseract
from docx import Document
import os

POPPLER_PATH = os.getenv("POPPLER_PATH", None)


def split_pdf_pages(pdf_path):
    if POPPLER_PATH:
        return convert_from_path(pdf_path, poppler_path=POPPLER_PATH)
    return convert_from_path(pdf_path)


def ocr_page(page_image, lang='eng'):
    text = pytesseract.image_to_string(page_image, lang=lang, config='--psm 6')
    return text.strip()


def combine_page_texts(page_texts, add_page_markers=True):
    full_text_parts = []

    for i, text in enumerate(page_texts, start=1):
        if add_page_markers:
            full_text_parts.append(f"--- Page {i} ---\n{text}")
        else:
            full_text_parts.append(text)

    return "\n\n".join(full_text_parts)


def ocr_pdf(pdf_path, output_txt_path=None, lang='eng', add_page_markers=True):
    pages = split_pdf_pages(pdf_path)

    page_texts = []
    for page in pages:
        text = ocr_page(page, lang=lang)
        page_texts.append(text)

    full_text = combine_page_texts(page_texts, add_page_markers=add_page_markers)

    if output_txt_path:
        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    return full_text


def save_as_docx(text, docx_path):
    doc = Document()
    for block in text.split("\n\n"):
        if block.strip():
            doc.add_paragraph(block.strip())
    doc.save(docx_path)


def ocr_folder(input_folder, output_folder, lang='eng'):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            print(f"[INFO] OCR sur : {filename}")

            base_name = os.path.splitext(filename)[0]
            output_txt_path = os.path.join(output_folder, base_name + '.txt')

            ocr_pdf(pdf_path, output_txt_path=output_txt_path, lang=lang)

            print(f"[INFO] Fichier OCR sauvegardé : {output_txt_path}")