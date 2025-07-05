import google.generativeai as genai
from typing import Literal
import os
class DocumentClassifier:
    """
    Classifies uploaded documents into types using Gemini Pro.
    """
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def classify_document(self, filename: str, text: str) -> Literal["bill", "discharge_summary", "id_card", "other"]:
        """
        Classify a document based on filename and content.
        
        Args:
            filename: Name of the uploaded file
            text: Extracted text from the document
            
        Returns:
            Document type classification
        """
        prompt = f"""
        Classify the following medical document into one of these categories:
        - bill
        - discharge_summary
        - id_card
        - other
        
        Filename: {filename}
        Content: {text[:5000]}  # Limiting to first 5000 chars for efficiency
        
        Return only the category name, nothing else.
        """
        
        try:
            response = self.model.generate_content(prompt)
            classification = response.text.lower().strip()
            
            # Validate the response
            valid_types = ["bill", "discharge_summary", "id_card", "other"]
            if classification in valid_types:
                return classification
            return "other"
        except Exception as e:
            print(f"Error classifying document: {e}")
            return "other"