import PyPDF2 
from typing import List, Dict
import io

async def process_uploaded_files(files: List) -> List[Dict]:
    
    processed_files = []
    
    for file in files:
        if file.content_type != "application/pdf":
            continue
            
        contents = await file.read()
        
        reader = PyPDF2.PdfReader(io.BytesIO(contents))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        processed_files.append({
            "filename": file.filename,
            "text": text
        })
        
    return processed_files