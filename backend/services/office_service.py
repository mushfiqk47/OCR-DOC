
import io
import os
import tempfile
import asyncio
import docx2pdf
from docx import Document
from docx.shared import Pt
from concurrent.futures import ThreadPoolExecutor

# Thread pool for blocking operations
_executor = ThreadPoolExecutor(max_workers=4)

class OfficeService:
    @staticmethod
    async def convert_text_to_word(text: str) -> bytes:
        """Convert plain text to a .docx file."""
        doc = Document()
        doc.add_paragraph(text)
        
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _convert_docx_to_pdf_sync(temp_docx_path: str, temp_pdf_path: str) -> None:
        """Synchronous function to convert docx to pdf - runs in thread pool"""
        import pythoncom
        pythoncom.CoInitialize()
        try:
            docx2pdf.convert(temp_docx_path, temp_pdf_path)
        finally:
            pythoncom.CoUninitialize()

    @staticmethod
    async def convert_word_to_pdf(docx_bytes: bytes) -> bytes:
        """Convert .docx to .pdf (Requires Word installed on Windows)."""
        # This is tricky because docx2pdf works on files, not streams.
        # And it requires Word to be installed (which is true for this user).
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
            temp_docx.write(docx_bytes)
            temp_docx_path = temp_docx.name
            
        temp_pdf_path = temp_docx_path.replace(".docx", ".pdf")
        
        try:
            # Run blocking docx2pdf in thread pool to avoid blocking event loop
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                _executor,
                OfficeService._convert_docx_to_pdf_sync,
                temp_docx_path,
                temp_pdf_path
            )
            
            with open(temp_pdf_path, "rb") as f:
                pdf_bytes = f.read()
                
            return pdf_bytes
        except Exception as e:
            raise Exception(f"Word conversion failed: {str(e)}")
        finally:
            # Cleanup
            if os.path.exists(temp_docx_path):
                os.remove(temp_docx_path)
            if os.path.exists(temp_pdf_path):
                os.remove(temp_pdf_path)
