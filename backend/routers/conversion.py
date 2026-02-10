
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response, JSONResponse
from typing import List
import io

from backend.services.conversion_service import ConversionService
from backend.services.barcode_service import BarcodeService
from backend.services.office_service import OfficeService
# Reuse existing services where possible
from backend.services.ollama_client import ollama_client 
from backend.services.pdf_service import render_pdf_to_images
from backend.services.image_service import image_to_base64, preprocess_image
from backend.services.translation_service import PdfTranslatorService
from PIL import Image

router = APIRouter(prefix="/api/convert", tags=["Conversion"])

# --- GROUP 1: Document Conversion ---

@router.post("/images-to-pdf")
async def images_to_pdf(files: List[UploadFile] = File(...)):
    image_bytes_list = []
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(400, "All files must be images")
        content = await file.read()
        image_bytes_list.append(content)
        
    pdf_bytes = await ConversionService.images_to_pdf(image_bytes_list)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=converted.pdf"})

@router.post("/text-to-pdf")
async def text_to_pdf(text: str = Form(...)):
    pdf_bytes = await ConversionService.text_to_pdf(text)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=converted.pdf"})

@router.post("/pdf-to-text")
async def pdf_to_text(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "File must be PDF")
    content = await file.read()
    text = await ConversionService.pdf_to_text(content)
    return JSONResponse({"text": text})

@router.post("/merge-pdf")
async def merge_pdf(files: List[UploadFile] = File(...)):
    pdf_bytes_list = []
    for file in files:
        if file.content_type != "application/pdf":
            raise HTTPException(400, "All files must be PDF")
        content = await file.read()
        pdf_bytes_list.append(content)
        
    merged_pdf = await ConversionService.merge_pdfs(pdf_bytes_list)
    return Response(content=merged_pdf, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=merged.pdf"})

@router.post("/html-to-pdf")
async def html_to_pdf(file: UploadFile = File(...)):
    # Can accept HTML file upload
    content = await file.read()
    html_str = content.decode("utf-8")
    pdf_bytes = await ConversionService.html_to_pdf(html_str)
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=converted.pdf"})

# --- GROUP 2: Office ---

@router.post("/text-to-word")
async def text_to_word(text: str = Form(...)):
    docx_bytes = await OfficeService.convert_text_to_word(text)
    return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=converted.docx"})

@router.post("/word-to-pdf")
async def word_to_pdf(file: UploadFile = File(...)):
     if "wordprocessingml" not in file.content_type and not file.filename.endswith(".docx"):
         raise HTTPException(400, "File must be .docx")
     content = await file.read()
     try:
         pdf_bytes = await OfficeService.convert_word_to_pdf(content)
         return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=converted.pdf"})
     except Exception as e:
         raise HTTPException(500, str(e))

@router.post("/jpg-to-word")
async def jpg_to_word(file: UploadFile = File(...)):
    # Reuse OCR logic: Image -> Text -> Word
    content = await file.read()
    # 1. Base64 encode
    # 2. Ollama OCR
    # 3. Text output -> Docx
    # Since we can't easily call other routers, we replicate logic or move logic to service in future refactor.
    # For now, let's just do a quick OCR -> Text implementation here for MVP.
    image = Image.open(io.BytesIO(content)).convert("RGB")
    # Resize if needed
    b64 = image_to_base64(image)
    text = await ollama_client.ocr_image(b64)
    
    docx_bytes = await OfficeService.convert_text_to_word(text)
    return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=ocr_converted.docx"})

@router.post("/pdf-to-word")
async def pdf_to_word(file: UploadFile = File(...)):
    # PDF -> Text -> Word (Simple version)
    # Advanced version would be PDF -> Images -> OCR -> Word OR PDF -> Text extraction -> Word
    content = await file.read()
    text = await ConversionService.pdf_to_text(content)
    docx_bytes = await OfficeService.convert_text_to_word(text)
    return Response(content=docx_bytes, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=converted.docx"})

# --- GROUP 3: Image Tools & Barcodes ---

# --- GROUP 3: Image Tools & Barcodes ---

@router.post("/invert-image")
async def invert_image(file: UploadFile = File(...)):
    content = await file.read()
    inverted_bytes = BarcodeService.invert_image(content)
    return Response(content=inverted_bytes, media_type="image/png")

@router.post("/text-to-image")
async def text_to_image(text: str = Form(...)):
    # Simple Text -> Image using PIL
    from PIL import ImageDraw, ImageFont
    
    # Estimate size
    lines = text.split('\n')
    max_len = max(len(line) for line in lines) if lines else 0
    font_size = 20
    width = max(600, max_len * 12)
    height = max(400, len(lines) * 30 + 100)
    
    img = Image.new('RGB', (width, height), color='white')
    d = ImageDraw.Draw(img)
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()
        
    d.text((50, 50), text, fill=(0, 0, 0), font=font)
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="image/png")

@router.post("/image-translator")
async def image_translator(file: UploadFile = File(...), target_language: str = Form("English")):
    # Reuse Translate logic: Image -> OCR -> Translate
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    img = preprocess_image(image)
    b64 = image_to_base64(img)
    
    original_text = await ollama_client.ocr_image(b64, prompt="Extract the text from this image.")
    translated_text = await ollama_client.translate_text(original_text, target_language)
    
    return JSONResponse({
        "original_text": original_text,
        "translated_text": translated_text
    })

@router.post("/qr-generator")
async def qr_generator(text: str = Form(...)):
    qr_bytes = BarcodeService.generate_qr(text)
    return Response(content=qr_bytes, media_type="image/png")

@router.post("/qr-scanner")
async def qr_scanner(file: UploadFile = File(...)):
    content = await file.read()
    result = BarcodeService.decode_qr(content)
    return JSONResponse({"text": result})

@router.post("/barcode-scanner")
async def barcode_scanner(file: UploadFile = File(...)):
    content = await file.read()
    result = BarcodeService.decode_barcode(content)
    return JSONResponse({"text": result})

# --- Pdf To Jpg (Reuse existing pdf_service logic) ---
@router.post("/pdf-to-jpg")
async def pdf_to_jpg(file: UploadFile = File(...)):
    content = await file.read()
    images = render_pdf_to_images(content)
    
    img = images[0]
    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)
    return Response(content=buffer.getvalue(), media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=page1.jpg"})

@router.post("/word-to-jpg")
async def word_to_jpg(file: UploadFile = File(...)):
    # Word -> PDF -> JPG
    if "wordprocessingml" not in file.content_type and not file.filename.endswith(".docx"):
         raise HTTPException(400, "File must be .docx")
    
    content = await file.read()
    try:
        # 1. Word -> PDF
        pdf_bytes = await OfficeService.convert_word_to_pdf(content)
        # 2. PDF -> Images
        images = render_pdf_to_images(pdf_bytes)
        # 3. Image -> JPG
        img = images[0]
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return Response(content=buffer.getvalue(), media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=converted.jpg"})
    except Exception as e:
        raise HTTPException(500, str(e))

# --- Excel Tools ---

@router.post("/jpg-to-excel")
async def jpg_to_excel(file: UploadFile = File(...)):
    # Image -> OCR (Table) -> Excel
    from backend.services.table_parser import parse_markdown_tables
    from backend.services.excel_service import dataframes_to_excel
    
    content = await file.read()
    image = Image.open(io.BytesIO(content))
    img = preprocess_image(image)
    b64 = image_to_base64(img)
    
    markdown = await ollama_client.ocr_image(b64, prompt="Extract the table from this image as a Markdown table.")
    tables = parse_markdown_tables(markdown)
    
    if not tables:
        raise HTTPException(400, "No tables found in image.")
        
    excel_bytes = dataframes_to_excel(tables)
    return Response(content=excel_bytes, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=converted.xlsx"})

@router.post("/pdf-to-excel")
async def pdf_to_excel(file: UploadFile = File(...)):
    # PDF -> Images -> OCR (Table) -> Excel
    from backend.services.table_parser import parse_markdown_tables
    from backend.services.excel_service import dataframes_to_excel
    
    content = await file.read()
    images = render_pdf_to_images(content)
    
    all_tables = []
    for img in images:
        b64 = image_to_base64(preprocess_image(img))
        markdown = await ollama_client.ocr_image(b64, prompt="Extract the table from this image as a Markdown table.")
        tables = parse_markdown_tables(markdown)
        all_tables.extend(tables)
        
    if not all_tables:
        raise HTTPException(400, "No tables found in PDF.")
        
    excel_bytes = dataframes_to_excel(all_tables)
    return Response(content=excel_bytes, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": "attachment; filename=converted.xlsx"})

@router.post("/pdf-to-csv")
async def pdf_to_csv(file: UploadFile = File(...)):
    # PDF -> Excel logic -> CSV (first table only or zip?)
    # For MVP, return first table as CSV
    from backend.services.table_parser import parse_markdown_tables
    import pandas as pd
    
    content = await file.read()
    images = render_pdf_to_images(content)
    
    # Process first page only for speed/MVP or all?
    # Let's do first page that has a table
    found_df = None
    for img in images:
        b64 = image_to_base64(preprocess_image(img))
        markdown = await ollama_client.ocr_image(b64, prompt="Extract the table from this image as a Markdown table.")
        tables = parse_markdown_tables(markdown)
        if tables:
            found_df = tables[0]
            break
            
    if found_df is None:
        raise HTTPException(400, "No tables found in PDF.")
        
    csv_str = found_df.to_csv(index=False)
    return Response(content=csv_str, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=converted.csv"})

@router.post("/excel-to-jpg")
async def excel_to_jpg(file: UploadFile = File(...)):
    # Excel -> Pandas -> HTML -> PDF -> JPG
    # Complex chain but robust given libraries
    import pandas as pd
    
    content = await file.read()
    try:
        # Load Excel using pandas (requires openpyxl)
        excel_data = pd.read_excel(io.BytesIO(content), sheet_name=None)
        
        # Take first sheet
        first_sheet_name = list(excel_data.keys())[0]
        df = excel_data[first_sheet_name]
        
        # Convert to HTML
        html_str = df.to_html()
        
        # HTML -> PDF
        pdf_bytes = await ConversionService.html_to_pdf(html_str)
        
        # PDF -> JPG
        images = render_pdf_to_images(pdf_bytes)
        img = images[0]
        
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG")
        buffer.seek(0)
        return Response(content=buffer.getvalue(), media_type="image/jpeg", headers={"Content-Disposition": "attachment; filename=converted.jpg"})
        
    except Exception as e:
        raise HTTPException(500, f"Conversion failed: {str(e)}")

@router.post("/pdf-to-html")
async def pdf_to_html(file: UploadFile = File(...)):
    # PDF -> Text -> HTML (Basic)
    content = await file.read()
    text = await ConversionService.pdf_to_text(content)
    
    # Simple HTML wrapper
    html = f"""
    <html>
    <head>
        <title>Converted PDF</title>
        <style>body {{ font-family: Arial, sans-serif; white-space: pre-wrap; padding: 20px; }}</style>
    </head>
    <body>
        {text}
    </body>
    </html>
    """
    return Response(content=html, media_type="text/html", headers={"Content-Disposition": "attachment; filename=converted.html"})

@router.post("/pdf-translator")
async def pdf_translator(file: UploadFile = File(...), target_language: str = Form("Spanish")):
    # PDF -> Images -> Layout Analysis -> Translate -> Reconstruct PDF
    if file.content_type != "application/pdf":
        raise HTTPException(400, "File must be PDF")
        
    content = await file.read()
    try:
        pdf_bytes = await PdfTranslatorService.translate_pdf(content, target_language)
        return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=translated.pdf"})
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(500, f"Translation failed: {str(e)}")

