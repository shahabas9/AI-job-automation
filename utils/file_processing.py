import io
import pdfplumber
import docx

def extract_text_from_file(file_content: bytes, filename: str) -> str:
    """
    Extracts text from PDF, DOCX, or TXT files.
    """
    filename = filename.lower()
    
    if filename.endswith(".pdf"):
        return _extract_from_pdf(file_content)
    elif filename.endswith(".docx"):
        return _extract_from_docx(file_content)
    else:
        # Assume text/plain
        try:
            return file_content.decode("utf-8")
        except UnicodeDecodeError:
            # Fallback for other encodings if needed, or raise
            return file_content.decode("latin-1")

def _extract_from_pdf(file_content: bytes) -> str:
    text_content = []
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                text_content.append(text)
    return "\n".join(text_content)

def _extract_from_docx(file_content: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_content))
    return "\n".join([para.text for para in doc.paragraphs])
