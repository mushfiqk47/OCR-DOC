from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse, JSONResponse
from backend.services.ollama_client import ollama_client
from backend.services.image_service import preprocess_image, image_to_base64
from backend.services.pdf_service import render_pdf_to_images
from backend.services.table_parser import parse_markdown_tables
from backend.services.table_merger import merge_tables
from backend.services.excel_service import dataframes_to_excel
from PIL import Image
import io
import uuid
import os
import tempfile
import shutil
import asyncio

router = APIRouter(prefix="/api/ocr", tags=["Table Extraction"])

# Use system temp directory for generated Excel files with project subdirectory
TEMP_DIR = os.path.join(tempfile.gettempdir(), "docintel_exports")
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/table")
async def extract_table(file: UploadFile = File(...)):
    """
    Extracts tables from document, merges them, and returns Excel download URL + JSON preview.
    """
    if file.content_type not in ["image/jpeg", "image/png", "application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type.")

    images = []
    content = await file.read()

    if file.content_type == "application/pdf":
        images = render_pdf_to_images(content)
    else:
        images = [preprocess_image(Image.open(io.BytesIO(content)))]

    all_tables = []
    
    # Process each page
    for img in images:
        base64_img = image_to_base64(img)
        # Prompt specifically for Markdown table output
        markdown_response = await ollama_client.ocr_image(
            base64_img,
            prompt="Extract the table from this image. Output strictly as a Markdown table. Do not include any other text."
        )
        
        page_tables = parse_markdown_tables(markdown_response)
        all_tables.extend(page_tables)

    if not all_tables:
        return {"message": "No tables found", "preview_data": []}

    # Consolidated logic for table merging (if multiple tables found)
    # merged_tables = merge_tables(all_tables) 
    # For now, let's keep them separate or use the merger if they look like continuations
    # To keep it simple for the MVP, we'll try to merge indiscriminately if they match headers
    final_tables = merge_tables(all_tables)

    # Generate Excel
    excel_bytes = dataframes_to_excel(final_tables)
    
    # Save to temp file
    filename = f"{uuid.uuid4()}.xlsx"
    filepath = os.path.join(TEMP_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(excel_bytes)
    
    # Prepare preview (limit to first 5 rows of first table)
    preview = []
    if final_tables:
        preview = final_tables[0].head(5).to_dict(orient="records")

    return {
        "message": "Tables extracted successfully",
        "download_url": f"/api/ocr/download/{filename}",
        "preview_data": preview,
        "total_tables": len(final_tables)
    }

@router.get("/download/{filename}")
async def download_file(filename: str, background_tasks: BackgroundTasks):
    filepath = os.path.join(TEMP_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Cleanup task - remove file after response is sent
    async def cleanup_file(path: str):
        try:
            await asyncio.sleep(1)  # Brief delay to ensure file is fully sent
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass  # Ignore cleanup errors
    
    background_tasks.add_task(cleanup_file, filepath)
    
    return FileResponse(filepath, filename="extracted_tables.xlsx", media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# Cleanup old temp files on startup
@router.on_event("startup")
async def cleanup_old_temp_files():
    """Remove old temp files from previous runs on startup"""
    try:
        if os.path.exists(TEMP_DIR):
            for filename in os.listdir(TEMP_DIR):
                filepath = os.path.join(TEMP_DIR, filename)
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                except Exception:
                    pass  # Ignore individual file cleanup errors
    except Exception:
        pass  # Ignore cleanup errors
