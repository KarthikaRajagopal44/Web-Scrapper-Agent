from fastapi import FastAPI, status
from src.schemas.request import ExtractionRequest
from src.services.scraper import ScraperService
from src.services.extractor import ExtractorService

app = FastAPI(
    title="Intelligent Web Scraper & Entity Extractor",
    version="1.0.0",
    description="Production-grade API to ingest, clean, and extract structured JSON schemas from webpages."
)

# Instantiate the service
extractor_service = ExtractorService()

@app.post(
    "/v1/extract", 
    status_code=status.HTTP_200_OK,
    summary="Extract structured entities from a URL",
    response_description="A validated JSON object conforming to the requested schema."
)
async def extract_url_data(payload: ExtractionRequest):
    # Step 1: Fetch and clean webpage asynchronously
    cleaned_text = await ScraperService.fetch_and_clean(str(payload.url))
    
    # Step 2: Extract structured data from cleaned text using Gemini
    extracted_data = await extractor_service.extract_structured_data(
        text=cleaned_text,
        extraction_type=payload.extraction_type
    )
    
    return extracted_data