# Medical Insurance Claim Processor

An AI-powered system for processing medical insurance claims using FastAPI and Gemini AI.

## Features

- PDF document processing
- AI-based document classification
- Specialized agents for different document types
- Data validation and consistency checking
- Claim decision automation

## Architecture

The system follows a modular architecture with these components:

1. **FastAPI Backend**: Handles file uploads and orchestrates the processing pipeline
2. **Document Classifier**: Uses Gemini AI to classify uploaded documents
3. **Specialized Agents**: Process specific document types (bills, discharge summaries, ID cards)
4. **Validator**: Checks for missing documents and data consistency
5. **Decision Engine**: Makes approve/reject decisions based on validation results

## AI Tools Used

1. **Cursor AI**: Used for:
   - Generating boilerplate FastAPI code
   - Creating test cases
   - Debugging async issues in the file upload handler

   Example prompts:
   - "Create a FastAPI endpoint that accepts multiple PDF files and processes them asynchronously"
   - "Generate pytest cases for testing file uploads with missing documents"

2. **Gemini Pro**: Used for:
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