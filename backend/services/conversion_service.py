
import io
import img2pdf
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa
import asyncio
from backend.services.pdf_service import render_pdf_to_images
from backend.services.ollama_client import ollama_client
from backend.services.image_service import image_to_base64, preprocess_image

class ConversionService:
    @staticmethod
    async def images_to_pdf(image_files: list[bytes]) -> bytes:
        """Convert a list of image bytes to a single PDF."""
        # img2pdf requires direct bytes or file paths. 
        # It handles JPEG/PNG metrics better than PIL for PDF generation.
        # However, for consistency and stripping alpha channels if needed, PIL is safer intermediate
        # but img2pdf is loseless for JPEGs. 
        # Let's try direct img2pdf first for JPEGs, falling back to PIL for others.
        # Actually, let's just use img2pdf for everything if possible, or PIL.
        # PIL convert('RGB') is robust.
        
        pdf_bytes = img2pdf.convert(image_files)
        return pdf_bytes

    @staticmethod
    async def text_to_pdf(text: str) -> bytes:
        """Convert plain text to PDF."""
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        text_object = c.beginText(40, height - 40)
        text_object.setFont("Helvetica", 12)
        
        # Simple text wrapping
        import textwrap
        lines = text.split('\n')
        for line in lines:
            wrapped_lines = textwrap.wrap(line, width=90) # approx char width
            for wrapped in wrapped_lines:
                text_object.textLine(wrapped)
                
        c.drawText(text_object)
        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    async def pdf_to_text(pdf_bytes: bytes) -> str:
        """
        Extract text from PDF using High-Fidelity OCR.
        Renders pages to images and uses the configured OCR model.
        """
        images = render_pdf_to_images(pdf_bytes)
        
        full_text = []
        
        # Semaphore to limit concurrent Ollama requests
        sem = asyncio.Semaphore(5)

        async def process_page(index, img):
            async with sem:
                # Preprocess and encode
                processed_img = preprocess_image(img)
                b64 = image_to_base64(processed_img)
                # Perform OCR
                # We use a specific prompt for pure text extraction
                page_text = await ollama_client.ocr_image(
                    b64, 
                    prompt="Extract the text content from this page. Return raw text with Markdown formatting for structure. Do not include commentary."
                )
                return index, page_text

        tasks = [process_page(i, img) for i, img in enumerate(images)]
        
        if tasks:
            results = await asyncio.gather(*tasks)
            # Sort by index to ensure page order
            results.sort(key=lambda x: x[0])
            full_text = [r[1] for r in results]
            
        return "\n\n--- Page Break ---\n\n".join(full_text)

    @staticmethod
    async def merge_pdfs(pdf_files: list[bytes]) -> bytes:
        """Merge multiple PDF files into one."""
        merger = PdfWriter()
        for pdf_bytes in pdf_files:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            for page in reader.pages:
                merger.add_page(page)
        
        buffer = io.BytesIO()
        merger.write(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    async def html_to_pdf(html_content: str) -> bytes:
        """Convert HTML string to PDF."""
        buffer = io.BytesIO()
        pisa_status = pisa.CreatePDF(html_content, dest=buffer)
        if pisa_status.err:
            raise Exception("HTML to PDF conversion failed")
        buffer.seek(0)
        return buffer.getvalue()
