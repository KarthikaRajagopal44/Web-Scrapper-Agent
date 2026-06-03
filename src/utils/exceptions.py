from fastapi import HTTPException, status

class ScrapingException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail=detail)

class ExtractionException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)