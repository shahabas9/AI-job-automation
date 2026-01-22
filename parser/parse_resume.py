import pdfplumber

def extract_text(pdf_path: str) -> str:
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


if __name__ == "__main__":
    resume_text = extract_text("resume_intelligence/MOHAMED_SHAHABAS.pdf")
    with open("resume_text.txt", "w") as f:
        f.write(resume_text)

    print("✅ Resume text extracted")
