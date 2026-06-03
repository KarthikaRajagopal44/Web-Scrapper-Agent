from typing import Literal
from pydantic import BaseModel, HttpUrl

class ExtractionRequest(BaseModel):
    url: HttpUrl
    extraction_type: Literal["e_commerce_product", "legal_compliance"]