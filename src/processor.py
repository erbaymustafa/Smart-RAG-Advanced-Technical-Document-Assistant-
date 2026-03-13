import os
import fitz
import io
import easyocr
import numpy as np
from PIL import Image

# OCR motorunu başlat
reader = easyocr.Reader(['tr', 'en'])

def process_document(uploaded_file):
    filename = uploaded_file.filename
    file_extension = os.path.splitext(filename)[1].lower()
    
    # FastAPI üzerinden gelen dosyayı oku
    file_content = uploaded_file.file.read()
    
    if file_extension == '.pdf':
        doc = fitz.open(stream=file_content, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    elif file_extension in ['.png', '.jpg', '.jpeg']:
        image = Image.open(io.BytesIO(file_content))
        image_np = np.array(image)
        
        # y_ths=0.5: Sütunlu veya kutucuklu yapılarda dikeyde paragraf birleştirme hassasiyeti.
        # Bu ayar, Volkanlar görselindeki gibi dağılmış metinleri daha toplu okur.
        result = reader.readtext(image_np, detail=0, paragraph=True, y_ths=0.5)
        
        # Paragraflar arasına çift satır koyarak LLM'in (Llama3) yapıyı anlamasını kolaylaştırır
        return "\n\n".join(result)
    
    return "Desteklenmeyen format."