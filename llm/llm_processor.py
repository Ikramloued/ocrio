import os
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434")


def get_llm(llm_type: str):
    if llm_type == "arabic":
        return Ollama(
            model="command-r7b-arabic:latest",
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )

    elif llm_type == "latin":
        return Ollama(
            model="deepseek-r1:14b",
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )

    elif llm_type == "multilingual":
        return Ollama(
            model="deepseek-r1:14b",
            temperature=0.1,
            base_url=OLLAMA_BASE_URL
        )

    return None


def process_with_llm(text: str, llm_type: str):
    if llm_type == "none":
        return text

    llm = get_llm(llm_type)
    if llm is None:
        return text

    if llm_type == "arabic":
        prompt = PromptTemplate(
            template="""
أنت مساعد متخصص في تحسين النصوص المستخرجة بتقنية OCR وتحويلها إلى نصوص رسمية ومنظمة.

المهام:
1. تصحيح أخطاء OCR.
2. إعادة تنظيم الفقرات بشكل منطقي وواضح.
3. الحفاظ على اللغة العربية الفصحى.
4. عدم إضافة أي معلومات جديدة.
5. عدم الترجمة إلى لغة أخرى.

النص الأصلي:
{text}

المطلوب:
- إعادة كتابة النص بشكل رسمي ومنسق.
- الحفاظ على المعنى الأصلي.
""",
            input_variables=["text"]
        )

    elif llm_type == "latin":
        prompt = PromptTemplate(
            template="""
You are an assistant specialized in cleaning OCR-extracted text and transforming it into a polished, professional text.

Tasks:
1. Fix OCR errors.
2. Organize paragraphs clearly.
3. Preserve the original language of each passage (French or English).
4. Do NOT add any new information.
5. Do NOT translate.

Original text:
{text}

Output:
- Rewrite the text clearly and professionally.
- Keep the same language as the original passage.
""",
            input_variables=["text"]
        )

    else:  # multilingual
        prompt = PromptTemplate(
            template="""
You are an assistant specialized in post-processing OCR text extracted from multilingual scanned documents.

The document may contain Arabic, French, and English.

Tasks:
1. Correct OCR errors carefully.
2. Reorganize the text into clean paragraphs.
3. Preserve the original language of each passage.
4. Do NOT translate.
5. Do NOT add any new information.
6. Keep names, dates, references, and numbers as faithfully as possible.

Original OCR text:
{text}

Output:
Return a clean, well-structured version of the same document, preserving each section in its original language.
""",
            input_variables=["text"]
        )

    chain = prompt | llm | StrOutputParser()
    return chain.invoke({"text": text})