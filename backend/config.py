import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OCR_MODEL: str = "docai-ocr"
    TRANSLATION_MODEL: str = "translategemma:4b"
    PDF_DPI: int = 300
    MAX_FILE_SIZE_MB: int = 50

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
