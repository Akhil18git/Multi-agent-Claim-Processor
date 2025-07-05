from pydantic import BaseModel
from typing import List, Optional, Dict

class BillDocument(BaseModel):
    type: str = "bill"
    hospital_name: str
    total_amount: float
    date_of_service: str
    procedure_codes: Optional[List[str]] = None
    itemized_charges: Optional[List[Dict[str, float]]] = None

class DischargeDocument(BaseModel):
    type: str = "discharge_summary"
    patient_name: str
    diagnosis: str
    admission_date: str
    discharge_date: str
    treatment_summary: Optional[str] = None
    attending_physician: Optional[str] = None

class IDDocument(BaseModel):
    type: str = "id_card"
    patient_name: str
    policy_number: str
    insurance_provider: str
    effective_date: str
    expiration_date: Optional[str] = None

class ValidationResult(BaseModel):
    missing_documents: List[str]
    discrepancies: List[str]

class ClaimDecision(BaseModel):
    status: str  
    reason: str

class ClaimOutput(BaseModel):
    documents: List[BillDocument | DischargeDocument | IDDocument]
    validation: ValidationResult
    claim_decision: ClaimDecision