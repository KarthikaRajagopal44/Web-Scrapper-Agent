from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class EcommerceProduct(BaseModel):
    product_name: Optional[str] = Field(None, description="The clean name of the product.")
    sku: Optional[str] = Field(None, description="Unique Stock Keeping Unit (SKU) code if visible.")
    price: Optional[str] = Field(None, description="Price of the product, ideally including currency symbol.")
    features: List[str] = Field(default_factory=list, description="List of key features or benefits.")
    specifications: Dict[str, Any] = Field(default_factory=dict, description="Detailed specifications, e.g., dimensions, weight.")

class LegalCompliance(BaseModel):
    company_name: Optional[str] = Field(None, description="The name of the company or legal entity.")
    compliance_status: Optional[str] = Field(None, description="The general compliance status, e.g., Compliant, Non-compliant, Warning.")
    identified_risks: List[str] = Field(default_factory=list, description="Specific legal risks, penalties, or compliance liabilities outlined.")
    clauses_analyzed: List[str] = Field(default_factory=list, description="Important compliance clauses or policies reviewed.")
    summary: Optional[str] = Field(None, description="A high-level summary of the compliance text.")