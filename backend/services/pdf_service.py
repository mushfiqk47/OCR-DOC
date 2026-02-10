import pypdfium2 as pdfium
from PIL import Image
from backend.config import settings

def render_pdf_to_images(pdf_bytes: bytes) -> list[Image.Image]:
    """
    Renders each page of a PDF bytes object into a PIL Image.
    Uses the configured DPI setting.
    """
    images = []
    pdf = None
    
    try:
        # Calculate scale factor (PDF points are 1/72 inch)
        # scale = desired_dpi / 72
        scale = settings.PDF_DPI / 72.0
        
        pdf = pdfium.PdfDocument(pdf_bytes)
        
        for i in range(len(pdf)):
            page = pdf[i]
            # Render to PIL Image
            # rev=True means standard RGBA
            bitmap = page.render(scale=scale) 
            pil_image = bitmap.to_pil()
            # Convert to RGB to ensure compatibility
            if pil_image.mode != "RGB":
                pil_image = pil_image.convert("RGB")
                
            images.append(pil_image)
    finally:
        # Ensure PDF document is properly closed to free resources
        if pdf is not None:
            pdf.close()
        
    return images
