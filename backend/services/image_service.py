from PIL import Image
import io
import base64

def preprocess_image(img: Image.Image, max_dim: int = 2048) -> Image.Image:
    """
    Resize image if larger than max_dim, preserving aspect ratio.
    Enhance compatibility with GLM-OCR input expectations.
    """
    width, height = img.size
    if max(width, height) > max_dim:
        scale = max_dim / max(width, height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    # Ensure RGB (strip alpha channel if present)
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
        
    return img

def image_to_base64(img: Image.Image) -> str:
    """Convert PIL Image to Base64 string."""
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=95)
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
