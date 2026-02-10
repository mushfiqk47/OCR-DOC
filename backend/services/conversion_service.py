
import io
import img2pdf
from PIL import Image
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from xhtml2pdf import pisa

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
        """Extract text from PDF (simple extraction)."""
        reader = PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text

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
