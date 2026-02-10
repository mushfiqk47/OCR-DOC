import io
import asyncio
import markdown
from PIL import Image
from xhtml2pdf import pisa
from backend.services.pdf_service import render_pdf_to_images
from backend.services.ollama_client import ollama_client
from backend.services.image_service import image_to_base64, preprocess_image
from backend.config import settings

class PdfTranslatorService:
    @staticmethod
    async def translate_pdf(pdf_bytes: bytes, target_lang: str = "Spanish") -> bytes:
        """
        New Pipeline:
        1. Render PDF to images.
        2. OCR each page to Markdown text.
        3. Insert [Image Page X] placeholders.
        4. Translate the Markdown content.
        5. Convert Translated Markdown to a "Preview Mode" PDF.
        """
        
        # 1. Render PDF to images
        images = render_pdf_to_images(pdf_bytes)
        
        # 2. Extract Markdown content using OCR
        md_pages = []
        sem = asyncio.Semaphore(5)

        async def ocr_page(idx, img):
            async with sem:
                processed = preprocess_image(img)
                b64 = image_to_base64(processed)
                # Specific prompt to get structured markdown
                text = await ollama_client.ocr_image(
                    b64, 
                    prompt="Extract all text from this page. Use Markdown for structure. Do not describe the layout. If there are charts or complex images, just ignore them, as I will add a placeholder."
                )
                return idx, text

        tasks = [ocr_page(i, img) for i, img in enumerate(images)]
        if tasks:
            results = await asyncio.gather(*tasks)
            results.sort(key=lambda x: x[0])
            for idx, text in results:
                # Add [Image Page X] as requested
                page_content = f"### [Image Page {idx + 1}]\n\n{text}"
                md_pages.append(page_content)

        full_md_content = "\n\n---\n\n".join(md_pages)

        # 3. Translate the full Markdown content
        # We split by page to avoid token limits and keep it manageable
        translated_md_pages = []
        
        async def translate_page(text):
            async with sem:
                return await ollama_client.translate_text(text, target_lang)

        translation_tasks = [translate_page(p) for p in md_pages]
        if translation_tasks:
            translated_results = await asyncio.gather(*translation_tasks)
            translated_md_pages = translated_results

        final_translated_md = "\n\n---\n\n".join(translated_md_pages)

        # 4. Convert MD to HTML with "Preview Mode" styling
        html_content = markdown.markdown(final_translated_md, extensions=['extra', 'codehilite'])
        
        styled_html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                @page {{
                    size: letter;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Helvetica', 'Arial', sans-serif;
                    line-height: 1.6;
                    color: #333;
                    background-color: #fff;
                }}
                h1, h2, h3 {{
                    color: #2c3e50;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 0.3em;
                }}
                hr {{
                    border: 0;
                    border-top: 1px solid #ccc;
                    margin: 2em 0;
                    page-break-after: always;
                }}
                pre {{
                    background-color: #f8f8f8;
                    padding: 1em;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                    font-family: 'Courier New', Courier, monospace;
                }}
                blockquote {{
                    border-left: 4px solid #ddd;
                    padding-left: 1em;
                    color: #777;
                    font-style: italic;
                }}
                table {{
                    border-collapse: collapse;
                    width: 100%;
                    margin-bottom: 1em;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .page-label {{
                    color: #95a5a6;
                    font-size: 0.9em;
                    margin-bottom: 1em;
                    font-weight: bold;
                }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """

        # 5. Convert HTML to PDF
        output_pdf_io = io.BytesIO()
        pisa_status = pisa.CreatePDF(styled_html, dest=output_pdf_io)
        
        if pisa_status.err:
             # Fallback if pisa fails
             return pdf_bytes
             
        return output_pdf_io.getvalue()