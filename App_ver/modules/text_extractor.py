from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    try:
        with open(file,"rb")as f:
            reader=PdfReader(f)
            text=''
            for page in reader.pages:
                text+=page.extract_text()+'\n'
            return text
    except:
        return f"Couldnt extract text"
    
def extract_text(file):
    try:
        with open(file,'r',encoding='utf-8') as f:
            text=f.read()
        return text
    except:
        return f"Couldnt extract text"
    