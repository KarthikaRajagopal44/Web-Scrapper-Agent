# Intelligent Web Scraper & Entity Extractor

A production-grade, highly scalable asynchronous FastAPI microservice designed to ingest web pages, strip structural DOM noise, and extract strictly-typed, schema-validated JSON structures using Large Language Models (LLMs) .

---

## 🏗️ System Architecture & Data Pipeline

The microservice follows a modular design pattern that separates concerns into routers, validation schemas, data parsing services, and LLM orchestration layers .

```text
[Client Request] ──(POST /v1/extract)──► [FastAPI Router]
                                                │
                                                ▼ (Asynchronous)
                                      [Scraper Service] (HTTPX Async Client)
                                                │
                                                ▼
                                      [BeautifulSoup Parser] (Noise Reduction)
                                                │
                                                ▼
                                      [Extractor Service] (Context Truncation)
                                                │
                                                ▼
                                      [LangChain Orchestrator] (.with_structured_output)
                                                │
                                                ▼
[Client Response] ◄──(JSON Output)─── [Gemini 3.5 Model] (Strict Pydantic Mapping)

Detailed Pipeline Phases:

API Entry & Validation (src/main.py):
Exposes a single asynchronous POST endpoint /v1/extract [page 1]. The incoming JSON payload is parsed and validated at the HTTP level using a Pydantic request schema (ExtractionRequest).
Asynchronous Ingestion (src/services/scraper.py):
An asynchronous, non-blocking HTTP GET request is dispatched using httpx.AsyncClient [page 2, 3]. Custom browser headers are passed to mimic a standard client and minimize the risk of anti-bot blocks.
DOM Noise Reduction (src/services/scraper.py):
Raw HTML contains heavy boilerplate (ads, styling, tracking, navigation). The HTML is parsed, and non-contextual tags (<script>, <style>, <nav>, <footer>, <header>, <aside>, <svg>, <noscript>, <iframe>) are programmatically targeted and decomposed [page 2, 3]. This reduces raw context size by up to 70–80%, saving significant API token costs and preventing LLM context clutter.
Structured LLM Parsing (src/services/extractor.py):
The cleaned text is checked against a maximum safe length threshold and truncated if necessary to prevent context window overflow [page 2, 3]. It is then fed to Google Gemini 3.5 using LangChain's native .with_structured_output() binding [page 2]. This forces the LLM to return structured parameters matching your target schema (EcommerceProduct or LegalCompliance) via native function-calling.
Exception Handling & Graceful Degradation (src/utils/exceptions.py):
If a website blocks the scraper, the URL is invalid, or parsing fails, custom exception classes catch the errors and convert them into clear, descriptive HTTP exception payloads rather than raising generic server crashes.

#  Project Directory Structure

intelligent-extractor/
├── .env                  # Environment secrets (Excluded from Git)
├── .env.example          # Sample environment template
├── requirements.txt      # Pinned dependency file
├── pyproject.toml        # Modern Python packaging configuration
├── README.md             # Project documentation & demo guide
└── src/
    ├── __init__.py
    ├── main.py           # FastAPI entry point & API Router
    ├── config.py         # App configurations & environment settings
    ├── schemas/
    │   ├── __init__.py
    │   ├── request.py    # Request payload validators
    │   └── extraction.py # Target Pydantic extraction schemas (E-commerce / Legal)
    ├── services/
    │   ├── __init__.py
    │   ├── scraper.py    # Async network fetcher & clean HTML parser
    │   └── extractor.py  # LLM structured output calling with context safeguards
    └── utils/
        ├── __init__.py
        └── exceptions.py # Structured custom API exception handlers

# Dependency Configurations

requirements.txt

fastapi>=0.110.0
uvicorn>=0.28.0
pydantic>=2.6.0
pydantic-settings>=2.2.0
httpx>=0.27.0
beautifulsoup4>=4.12.0
langchain-core>=0.1.30
langchain-google-genai>=1.0.1
python-dotenv>=1.0.1

# Local Setup & Environment Configuration

1. Configure Environment Secrets
Create a .env file in the root directory:

GOOGLE_API_KEY=your_gemini_api_key_here

# Install Dependencies
Set up a Python virtual environment and install the required libraries:

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

# Install requirements 
pip install -r requirements.txt

# Start the Local Server
Run the Uvicorn development server:

uvicorn src.main:app --reload
Once started, the interactive API documentation will be available at: http://127.0.0.1:8000/docs

# Demonstration & cURL Examples

You can test the asynchronous API endpoints directly using the following curl command lines in your terminal:
Case 1: Successful Extraction (E-commerce Product Schema)
This fetches a product description and extracts it into the strict EcommerceProduct schema

curl -X 'POST' \
  'http://127.0.0.1:8000/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://raw.githubusercontent.com/serkanyasr/agentic_rag_project/refs/heads/main/README.md",
  "extraction_type": "e_commerce_product"
}'

Expected Successful Output (200 OK):
{
  "product_name": "Agentic RAG Project",
  "sku": null,
  "price": null,
  "features": [
    "Pydantic AI-based intelligent agent system",
    "Multiple search strategies: Vector Search and Hybrid Search",
    "Advanced PDF processing: Table and image extraction with Docling",
    "Database: PostgreSQL + pgvector extension",
    "Real-time streaming: Live responses via Server-Sent Events",
    "Session management: Conversation history and context retention"
  ],
  "specifications": {
    "framework": "Pydantic AI",
    "database": "PostgreSQL",
    "orchestration": "Docker"
  }
}

# Case 2: Handled Failure Case (Graceful Error Recovery)
This sends a request to an unreachable domain to test our system's edge-case error resilience

curl -X 'POST' \
  'http://127.0.0.1:8000/v1/extract' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "url": "https://this-is-not-a-real-website-12345.com",
  "extraction_type": "e_commerce_product"
}'

Expected Failure Output (424 Failed Dependency):

{
  "detail": "Failed to connect to target webpage: [Errno -2] Name or service not known"
}

