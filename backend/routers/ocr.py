from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from backend.services.ollama_client import ollama_client
from backend.services.image_service import preprocess_image, image_to_base64
from backend.services.pdf_service import render_pdf_to_images
from PIL import Image
import io
import json

router = APIRouter(prefix="/api/ocr", tags=["OCR"])

@router.post("/text")
async def ocr_text(file: UploadFile = File(...)):
    """
    Extracts text from an uploaded image or PDF.
    Returns a Server-Sent Events (SSE) stream of the extracted text.
    """
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, PNG, and PDF are supported.")

    images = []
    content = await file.read()

    if file.content_type == "application/pdf":
        images = render_pdf_to_images(content)
    else:
        image = Image.open(io.BytesIO(content))
        images = [preprocess_image(image)]

    async def event_generator():
        try:
            for i, img in enumerate(images):
                # Send page header for multi-page docs
                if len(images) > 1:
                    yield json.dumps({"type": "progress", "page": i + 1, "total": len(images)}) + "\n"
                    yield json.dumps({"type": "content", "text": f"\n\n--- Page {i + 1} ---\n\n"}) + "\n"

                base64_img = image_to_base64(img)
                
                # Stream the OCR result for this page
                try:
                    async for token in ollama_client.ocr_image_stream(base64_img, prompt="Transcribe the text in this image. Use Markdown to denote headers (**), lists (-), and bold elements. Do not describe the layout."):
                        yield json.dumps({"type": "content", "text": token}) + "\n"
                except Exception as e:
                    yield json.dumps({"type": "error", "message": f"OCR failed on page {i + 1}: {str(e)}"}) + "\n"
                    return
            
            yield json.dumps({"type": "done"}) + "\n"
        except Exception as e:
            yield json.dumps({"type": "error", "message": f"Processing failed: {str(e)}"}) + "\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
