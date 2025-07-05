from typing import List, Dict

class ClaimValidator:
    
    REQUIRED_DOCUMENTS = ["id_card", "bill", "discharge_summary"]
    
    def validate(self, documents: List[Dict]) -> Dict:
        doc_types = [doc["type"] for doc in documents]
        missing_docs = [doc for doc in self.REQUIRED_DOCUMENTS if doc not in doc_types]
        
        discrepancies = self._check_consistency(documents)
        
        return {
            "missing_documents": missing_docs,
            "discrepancies": discrepancies
        }
    
    def _check_consistency(self, documents: List[Dict]) -> List[str]:
        
        discrepancies = []
        
        id_data = next((doc for doc in documents if doc["type"] == "id_card"), None)
        bill_data = next((doc for doc in documents if doc["type"] == "bill"), None)
        discharge_data = next((doc for doc in documents if doc["type"] == "discharge_summary"), None)
        
        if id_data and discharge_data:
            if id_data["patient_name"] and discharge_data["patient_name"]:
                if id_data["patient_name"].lower() != discharge_data["patient_name"].lower():
                    discrepancies.append("Patient name mismatch between ID card and discharge summary")
        
        if bill_data and discharge_data:
            if bill_data["date_of_service"] and discharge_data["discharge_date"]:
                if bill_data["date_of_service"] != discharge_data["discharge_date"]:
                    discrepancies.append("Service date on bill doesn't match discharge date")
        
        return discrepancies