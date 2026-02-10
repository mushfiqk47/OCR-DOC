from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.services.ollama_client import ollama_client
from backend.services.image_service import preprocess_image, image_to_base64
from backend.services.pdf_service import render_pdf_to_images
from PIL import Image
import io
from pydantic import BaseModel

router = APIRouter(prefix="/api/ocr", tags=["Translation"])

class TranslationResponse(BaseModel):
    original_text: str
    translated_text: str
    page: int

@router.post("/translate")
async def translate_document(
    file: UploadFile = File(...),
    target_language: str = Form(...)
):
    """
    Extracts text from image/PDF and translates it to target language.
    """
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    images = []
    content = await file.read()

    if file.content_type == "application/pdf":
        images = render_pdf_to_images(content)
    else:
        images = [preprocess_image(Image.open(io.BytesIO(content)))]

    results = []
    
    # Process sequentially to avoid OOM
    for i, img in enumerate(images):
        # Stage 1: Local OCR
        base64_img = image_to_base64(img)
        original_text = await ollama_client.ocr_image(
            base64_img, 
            prompt="Extract the text from this image exactly as it appears. Maintain all Markdown formatting. Do not translate."
        )
        
        # Stage 2: Translation
        translated_text = await ollama_client.translate_text(original_text, target_language)
        
        results.append({
            "page": i + 1,
            "original_text": original_text,
            "translated_text": translated_text
        })

    return {"pages": results}
