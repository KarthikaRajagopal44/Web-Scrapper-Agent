from typing import Type, Union
from pydantic import BaseModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.config import settings
from src.schemas.extraction import EcommerceProduct, LegalCompliance
from src.utils.exceptions import ExtractionException, ModelUnavailableException

class ExtractorService:
    def __init__(self):
    
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.0  
        )

    @staticmethod
    def _truncate_text(text: str, max_length: int) -> str:
        
        if len(text) > max_length:
            return text[:max_length] + "... [Text truncated for context-size safety]"
        return text

    async def extract_structured_data(
        self, 
        text: str, 
        extraction_type: str
    ) -> Union[EcommerceProduct, LegalCompliance]:
        
        # Selecting target schema based on payload
        if extraction_type == "e_commerce_product":
            schema: Type[BaseModel] = EcommerceProduct
            system_prompt = (
                "You are an expert data extraction bot. Your task is to extract "
                "e-commerce product information from the provided text. Fill in the "
                "fields exactly. If any information is missing, do not hallucinate—return null."
            )
        else:
            schema = LegalCompliance
            system_prompt = (
                "You are an expert legal compliance compliance analyst. Your task is to extract "
                "compliance indicators, clauses, risks, and overview data from the text. "
                "Do not make up facts; return null for any field not explicitly mentioned."
            )

        truncated_text = self._truncate_text(text, settings.MAX_TEXT_LENGTH)

        # Setting up a structured message prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("user", "Source Text:\n\n{input_text}\n\nPerform extraction strictly conforming to the requested schema.")
        ])

        try:
            # Binding the strict Pydantic model directly to the LLM
            structured_llm = self.llm.with_structured_output(schema)
            chain = prompt | structured_llm
            
            # Invoke the LLM call asynchronously (non-blocking)
            response = await chain.ainvoke({"input_text": truncated_text})
            return response
        except Exception as e:
            error_text = str(e)
            if "503" in error_text or "UNAVAILABLE" in error_text.upper() or "high demand" in error_text.lower() or "rate limit" in error_text.lower():
                raise ModelUnavailableException(
                    f"LLM service unavailable: {error_text}"
                )
            raise ExtractionException(f"Failed to parse or extract structured data: {error_text}")