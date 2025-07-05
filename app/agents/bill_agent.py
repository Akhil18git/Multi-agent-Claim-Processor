import google.generativeai as genai
from app.models.schemas import BillDocument
import re
import json
import os
class BillAgent:
    """
    Processes medical bill documents to extract structured information.
    """
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process(self, text: str) -> dict:
        """
        Extract structured information from medical bill text.
        
        Args:
            text: Extracted text from the bill document
            
        Returns:
            Dictionary with structured bill information
        """
        prompt = f"""
        Extract the following information from this medical bill:
        - hospital_name
        - total_amount (as float)
        - date_of_service (YYYY-MM-DD format)
        - procedure_codes (list of procedure codes if available)
        - itemized_charges (list of dictionaries with service and amount if available)
        
        Return ONLY a valid JSON object with these fields. Don't include any other text.
        
        Medical bill text:
        {text[:10000]}  # Limiting to first 10000 chars for efficiency
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Clean the response to extract just the JSON
            json_str = response.text.strip()
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            data = json.loads(json_str)
            
            # Convert to our schema
            bill_data = {
                "type": "bill",
                "hospital_name": data.get("hospital_name", ""),
                "total_amount": float(data.get("total_amount", 0)),
                "date_of_service": data.get("date_of_service", ""),
                "procedure_codes": data.get("procedure_codes", []),
                "itemized_charges": data.get("itemized_charges", [])
            }
            
            return bill_data
            
        except Exception as e:
            print(f"Error processing bill: {e}")
            return {
                "type": "bill",
                "hospital_name": "",
                "total_amount": 0,
                "date_of_service": "",
                "procedure_codes": [],
                "itemized_charges": []
            }