import google.generativeai as genai
import json
import os
class IDAgent:
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process(self, text: str) -> dict:
       
        prompt = f"""
        Extract the following information from this insurance ID card:
        - patient_name
        - policy_number
        - insurance_provider
        - effective_date (YYYY-MM-DD format)
        - expiration_date (YYYY-MM-DD format if available)
        
        Return ONLY a valid JSON object with these fields. Don't include any other text.
        
        ID card text:
        {text[:5000]}  # Limiting to first 5000 chars for efficiency
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            json_str = response.text.strip()
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            data = json.loads(json_str)
            
            id_data = {
                "type": "id_card",
                "patient_name": data.get("patient_name", ""),
                "policy_number": data.get("policy_number", ""),
                "insurance_provider": data.get("insurance_provider", ""),
                "effective_date": data.get("effective_date", ""),
                "expiration_date": data.get("expiration_date", "")
            }
            
            return id_data
            
        except Exception as e:
            print(f"Error processing ID card: {e}")
            return {
                "type": "id_card",
                "patient_name": "",
                "policy_number": "",
                "insurance_provider": "",
                "effective_date": "",
                "expiration_date": ""
            }