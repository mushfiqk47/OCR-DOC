from pydantic import BaseModel
from typing import Optional

class OCRResponse(BaseModel):
    text: str

class TranslationRequest(BaseModel):
    target_language: str

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str

class TableExtractionResponse(BaseModel):
    markdown: str
    download_url: Optional[str] = None
    preview_data: list[dict] # Simplified JSON representation of table for frontend grid
