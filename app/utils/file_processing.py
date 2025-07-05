import PyPDF2 
from typing import List, Dict
import io

async def process_uploaded_files(files: List) -> List[Dict]:
    """
    Process uploaded PDF files and extract text content.
    
    Args:
        files: List of uploaded files
        
    Returns:
        List of dictionaries containing filename and extracted text
    """
    processed_files = []
    
    for file in files:
        if file.content_type != "application/pdf":
            continue
            
        # Read file content
        contents = await file.read()
        
        # Extract text from PDF
        reader = PyPDF2.PdfReader(io.BytesIO(contents))
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        processed_files.append({
            "filename": file.filename,
            "text": text
        })
        
    return processed_files