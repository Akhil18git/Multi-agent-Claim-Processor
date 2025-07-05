# Medical Insurance Claim Processor

An AI-powered system for processing medical insurance claims using FastAPI and Gemini AI.

## Features

- This AI-powered backend system automates medical insurance claim processing by:

- Accepting uploaded medical documents (bills, discharge summaries)

- Classifying & extracting key data using AI (Gemini LLM)

- Validating for completeness/accuracy

- Approving/Rejecting claims with clear reasons

## Architecture

The system follows a modular architecture with these components:

- FastAPI:	Backend server (handles PDF uploads/API responses)
- Google Gemini:	Reads documents and extracts structured data
- LangChain:	Manages AI workflows and prompts
- PDFplumber:	Extracts text from medical forms
- AsyncIO:	Processes multiple claims simultaneously

## AI Tools Used

**Gemini Pro**: Used for:
   - Document classification
   - Structured data extraction from documents
   - JSON schema validation

   Example prompts (see in agent code):
   - "Extract the following information from this medical bill..."
   - "Classify this document into one of these categories..."

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt