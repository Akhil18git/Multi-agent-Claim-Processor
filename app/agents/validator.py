from typing import List, Dict

class ClaimValidator:
    """
    Validates the processed claim data for completeness and consistency.
    """
    
    REQUIRED_DOCUMENTS = ["id_card", "bill", "discharge_summary"]
    
    def validate(self, documents: List[Dict]) -> Dict:
        """
        Validate the processed claim documents.
        
        Args:
            documents: List of processed documents
            
        Returns:
            Dictionary with validation results
        """
        # Check for missing required documents
        doc_types = [doc["type"] for doc in documents]
        missing_docs = [doc for doc in self.REQUIRED_DOCUMENTS if doc not in doc_types]
        
        # Check for data consistency between documents
        discrepancies = self._check_consistency(documents)
        
        return {
            "missing_documents": missing_docs,
            "discrepancies": discrepancies
        }
    
    def _check_consistency(self, documents: List[Dict]) -> List[str]:
        """
        Check for consistency between different documents.
        
        Args:
            documents: List of processed documents
            
        Returns:
            List of discrepancy messages
        """
        discrepancies = []
        
        # Get data from different documents
        id_data = next((doc for doc in documents if doc["type"] == "id_card"), None)
        bill_data = next((doc for doc in documents if doc["type"] == "bill"), None)
        discharge_data = next((doc for doc in documents if doc["type"] == "discharge_summary"), None)
        
        # Check name consistency
        if id_data and discharge_data:
            if id_data["patient_name"] and discharge_data["patient_name"]:
                if id_data["patient_name"].lower() != discharge_data["patient_name"].lower():
                    discrepancies.append("Patient name mismatch between ID card and discharge summary")
        
        # Check date consistency
        if bill_data and discharge_data:
            if bill_data["date_of_service"] and discharge_data["discharge_date"]:
                if bill_data["date_of_service"] != discharge_data["discharge_date"]:
                    discrepancies.append("Service date on bill doesn't match discharge date")
        
        return discrepancies