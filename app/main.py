import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from typing import List
from app.models.schemas import ClaimOutput
from app.utils.file_processing import process_uploaded_files
from app.agents.classifier import DocumentClassifier
from app.agents.validator import ClaimValidator
from app.agents.bill_agent import BillAgent
from app.agents.discharge_agent import DischargeAgent
from app.agents.id_agent import IDAgent
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Medical Claim Processor",
             description="AI-powered medical insurance claim processing system")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize agents
classifier = DocumentClassifier()
bill_agent = BillAgent()
discharge_agent = DischargeAgent()
id_agent = IDAgent()
validator = ClaimValidator()

@app.post("/process-claim", response_model=ClaimOutput)
async def process_claim(files: List[UploadFile] = File(...)):
    """
    Process medical insurance claim documents.
    
    Accepts multiple PDF files (e.g., bill, ID card, discharge summary)
    Returns structured claim data with validation and decision.
    """
    try:
        # 1. Process uploaded files
        file_contents = await process_uploaded_files(files)
        
        # 2. Classify documents
        classified_docs = []
        for file in file_contents:
            doc_type = classifier.classify_document(file["filename"], file["text"])
            classified_docs.append({
                "filename": file["filename"],
                "text": file["text"],
                "type": doc_type
            })
        
        # 3. Process with specialized agents
        processed_data = []
        for doc in classified_docs:
            if doc["type"] == "bill":
                processed_data.append(bill_agent.process(doc["text"]))
            elif doc["type"] == "discharge_summary":
                processed_data.append(discharge_agent.process(doc["text"]))
            elif doc["type"] == "id_card":
                processed_data.append(id_agent.process(doc["text"]))
        
        # 4. Validate claim
        validation_result = validator.validate(processed_data)
        
        # 5. Make claim decision
        claim_decision = {
            "status": "approved" if not validation_result["missing_documents"] and not validation_result["discrepancies"] else "rejected",
            "reason": "All required documents present and data is consistent" 
                      if not validation_result["missing_documents"] and not validation_result["discrepancies"]
                      else "Missing documents or data discrepancies found"
        }
        
        # 6. Prepare final output
        output = {
            "documents": processed_data,
            "validation": validation_result,
            "claim_decision": claim_decision
        }
        
        return output
        
    except Exception as e:
        logger.error(f"Error processing claim: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))