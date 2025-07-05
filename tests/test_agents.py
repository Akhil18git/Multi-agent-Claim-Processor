import pytest
from app.agents.classifier import DocumentClassifier
from app.agents.bill_agent import BillAgent
from app.agents.discharge_agent import DischargeAgent
from app.agents.id_agent import IDAgent
from app.agents.validator import ClaimValidator

@pytest.fixture
def classifier():
    return DocumentClassifier()

@pytest.fixture
def bill_agent():
    return BillAgent()

@pytest.fixture
def discharge_agent():
    return DischargeAgent()

@pytest.fixture
def id_agent():
    return IDAgent()

@pytest.fixture
def validator():
    return ClaimValidator()

def test_classifier(classifier):
    # Mock test since actual classification requires LLM
    result = classifier.classify_document("bill.pdf", "Hospital Bill\nTotal: $1000")
    assert result in ["bill", "discharge_summary", "id_card", "other"]

def test_bill_agent(bill_agent):
    # Mock test
    bill_text = "Hospital Bill\nHospital: ABC Medical\nTotal: $1250.00\nDate: 2024-04-10"
    result = bill_agent.process(bill_text)
    assert result["type"] == "bill"
    assert "hospital_name" in result

def test_validator(validator):
    documents = [
        {"type": "id_card", "patient_name": "John Doe"},
        {"type": "bill", "date_of_service": "2024-04-10"},
        {"type": "discharge_summary", "patient_name": "John Doe", "discharge_date": "2024-04-10"}
    ]
    
    result = validator.validate(documents)
    assert not result["missing_documents"]
    assert not result["discrepancies"]
    
    # Test with inconsistent data
    documents[2]["patient_name"] = "Jane Doe"
    result = validator.validate(documents)
    assert "Patient name mismatch" in result["discrepancies"][0]