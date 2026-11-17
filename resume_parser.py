
from pypdf import PdfReader

def extract_resume_text(pdf_file):

    text = ""

    reader = PdfReader(pdf_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text
