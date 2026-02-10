
import io
import pytesseract
from PIL import Image, ImageDraw, ImageFont
from backend.services.pdf_service import render_pdf_to_images
from backend.services.ollama_client import ollama_client
import textwrap
import asyncio
import uuid

class PdfTranslatorService:
    @staticmethod
    async def translate_pdf(pdf_bytes: bytes, target_lang: str = "Spanish") -> bytes:
        """
        Translates a PDF file while preserving layout.
        1. Render PDF to images (pypdfium2)
        2. OCR to get text blocks and coordinates (pytesseract)
        3. Group words into paragraphs
        4. Translate paragraphs (Ollama)
        5. Overlay translated text on images
        6. Convert back to PDF
        """
        
        # 1. Render PDF to images
        images = render_pdf_to_images(pdf_bytes)
        translated_images = []

        # Process each page
        for page_idx, img in enumerate(images):
            # 2. Get OCR Data (box, text, confidence)
            try:
                # Need explicit config for layout analysis if possible, but default usually works
                ocr_data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
            except pytesseract.TesseractNotFoundError:
                print("Tesseract not found. Returning original image.")
                translated_images.append(img)
                continue
            except Exception as e:
                print(f"OCR Error on page {page_idx}: {e}")
                translated_images.append(img)
                continue

            draw = ImageDraw.Draw(img, "RGBA")
            
            n_boxes = len(ocr_data['level'])
            
            blocks = {} # Key: "block_par", Value: {words: [], left, top, right, bottom}

            for i in range(n_boxes):
                text = ocr_data['text'][i].strip()
                # Level 5 is Word. We only care about words with content.
                if not text:
                    continue
                
                block_num = ocr_data['block_num'][i]
                par_num = ocr_data['par_num'][i]
                
                # key to group by paragraph within a block
                key = f"{block_num}_{par_num}"
                
                x = ocr_data['left'][i]
                y = ocr_data['top'][i]
                w = ocr_data['width'][i]
                h = ocr_data['height'][i]
                
                if key not in blocks:
                    blocks[key] = {
                        'words': [],
                        'left': x,
                        'top': y,
                        'right': x + w,
                        'bottom': y + h
                    }
                
                blocks[key]['words'].append(text)
                # Expand boundaries
                blocks[key]['left'] = min(blocks[key]['left'], x)
                blocks[key]['top'] = min(blocks[key]['top'], y)
                blocks[key]['right'] = max(blocks[key]['right'], x + w)
                blocks[key]['bottom'] = max(blocks[key]['bottom'], y + h)

            # 3. Translate Paragraphs
            # Prepare tasks logic
            tasks = []
            keys = []

            for key, block in blocks.items():
                original_text = " ".join(block['words'])
                # Only translate substantial text
                if len(original_text) < 3: 
                    continue
                tasks.append(ollama_client.translate_text(original_text, target_lang))
                keys.append(key)

            # Parallel execution
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            else:
                results = []

            translations_map = {}
            for k, res in zip(keys, results):
                if isinstance(res, Exception):
                    print(f"Translation failed for block {k}: {res}")
                    continue
                translations_map[k] = res

            # 4. Draw Layout
            try:
                # Try standard fonts
                font_name = "arial.ttf"
                base_font_size = 12
                font = ImageFont.truetype(font_name, base_font_size)
            except IOError:
                font = ImageFont.load_default()
                base_font_size = 10 # approximate

            for key, block in blocks.items():
                if key not in translations_map:
                    continue

                t_text = translations_map[key]
                x = block['left']
                y = block['top']
                w = block['right'] - block['left']
                h = block['bottom'] - block['top']
                
                # Draw white box background
                # Pad slightly
                draw.rectangle([x-2, y-2, block['right']+2, block['bottom']+2], fill=(255, 255, 255, 255))
                
                # Text Wrapping Logic
                # Estimate char width (approx 0.6 of font size usually)
                char_width_approx = base_font_size * 0.6
                chars_per_line = max(1, int(w / char_width_approx))
                
                wrapped_lines = textwrap.wrap(t_text, width=chars_per_line)
                
                # Simple vertical layout
                current_y = y
                for line in wrapped_lines:
                    # Check if we exceed height? For now just draw, overflow is better than hidden
                    draw.text((x, current_y), line, font=font, fill=(0, 0, 0, 255))
                    current_y += base_font_size * 1.2 # Line height

            translated_images.append(img.convert("RGB"))

        # 5. Convert back to PDF
        if not translated_images:
             return pdf_bytes 
             
        output_pdf_io = io.BytesIO()
        translated_images[0].save(
            output_pdf_io, 
            "PDF", 
            resolution=100.0, 
            save_all=True, 
            append_images=translated_images[1:]
        )
        return output_pdf_io.getvalue()
