import pytest
from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

@pytest.fixture
def sample_bill():
    return open("tests/sample_data/sample_bill.pdf", "rb")

@pytest.fixture
def sample_discharge():
    return open("tests/sample_data/sample_discharge.pdf", "rb")

@pytest.fixture
def sample_id():
    return open("tests/sample_data/sample_id.pdf", "rb")

def test_process_claim_with_all_documents(sample_bill, sample_discharge, sample_id):
    files = [
        ("files", ("bill.pdf", sample_bill, "application/pdf")),
        ("files", ("discharge.pdf", sample_discharge, "application/pdf")),
        ("files", ("id.pdf", sample_id, "application/pdf"))
    ]
    
    response = client.post("/process-claim", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["documents"]) == 3
    assert not data["validation"]["missing_documents"]
    assert data["claim_decision"]["status"] == "approved"

def test_process_claim_with_missing_documents(sample_bill):
    files = [
        ("files", ("bill.pdf", sample_bill, "application/pdf"))
    ]
    
    response = client.post("/process-claim", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["documents"]) == 1
    assert len(data["validation"]["missing_documents"]) > 0
    assert data["claim_decision"]["status"] == "rejected"

def test_process_claim_with_invalid_file():
    files = [
        ("files", ("test.txt", b"not a pdf", "text/plain"))
    ]
    
    response = client.post("/process-claim", files=files)
    
    assert response.status_code == 200
    data = response.json()
    
    assert len(data["documents"]) == 0
    assert len(data["validation"]["missing_documents"]) == 3