import google.generativeai as genai
import json
import os
class DischargeAgent:
    
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def process(self, text: str) -> dict:
       
        prompt = f"""
        Extract the following information from this hospital discharge summary:
        - patient_name
        - diagnosis
        - admission_date (YYYY-MM-DD format)
        - discharge_date (YYYY-MM-DD format)
        - treatment_summary (brief summary if available)
        - attending_physician (if available)
        
        Return ONLY a valid JSON object with these fields. Don't include any other text.
        
        Discharge summary text:
        {text[:10000]}  
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            json_str = response.text.strip()
            json_str = json_str.replace('```json', '').replace('```', '').strip()
            
            data = json.loads(json_str)
            
            discharge_data = {
                "type": "discharge_summary",
                "patient_name": data.get("patient_name", ""),
                "diagnosis": data.get("diagnosis", ""),
                "admission_date": data.get("admission_date", ""),
                "discharge_date": data.get("discharge_date", ""),
                "treatment_summary": data.get("treatment_summary", ""),
                "attending_physician": data.get("attending_physician", "")
            }
            
            return discharge_data
            
        except Exception as e:
            print(f"Error processing discharge summary: {e}")
            return {
                "type": "discharge_summary",
                "patient_name": "",
                "diagnosis": "",
                "admission_date": "",
                "discharge_date": "",
                "treatment_summary": "",
                "attending_physician": ""
            }