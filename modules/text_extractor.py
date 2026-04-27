from PyPDF2 import PdfReader

def extract_text(file):
    try:
        reader=PdfReader(file)
        text=''
        for page in reader.pages:
            text+=page.extract_text()+'\n'
        return text
    except Exception as e:
        return f"Couldnt extract text"
    