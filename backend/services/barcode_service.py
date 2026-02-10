
import qrcode
import cv2
import numpy as np
import io
from PIL import Image

class BarcodeService:
    @staticmethod
    def generate_qr(data: str) -> bytes:
        """Generate a QR code image."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def decode_qr(image_bytes: bytes) -> str:
        """Decode a QR code from an image."""
        # Convert bytes to numpy array for cv2
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        detector = cv2.QRCodeDetector()
        data, bbox, straight_qrcode = detector.detectAndDecode(img)
        
        if bbox is not None and data:
            return data
        return "No QR code detected"

    @staticmethod
    def decode_barcode(image_bytes: bytes) -> str:
        """Decode a 1D barcode from an image using OpenCV."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Try OpenCV's barcode detector (available in opencv-contrib or newer builds)
        try:
            barcode_detector = cv2.barcode.BarcodeDetector()
            retval, decoded_info, decoded_type, points = barcode_detector.detectAndDecode(img)
            if retval and decoded_info:
                results = [d for d in decoded_info if d]
                if results:
                    return results[0]
        except AttributeError:
            pass

        # Fallback: try QR detector as a catch-all
        detector = cv2.QRCodeDetector()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None and data:
            return data

        return "No barcode detected"

    @staticmethod
    def invert_image(image_bytes: bytes) -> bytes:
        """Invert image colors."""
        image = Image.open(io.BytesIO(image_bytes))
        
        # Handle alpha channel (transparency)
        if image.mode == 'RGBA':
            r, g, b, a = image.split()
            rgb_image = Image.merge('RGB', (r, g, b))
            inverted_image = Image.eval(rgb_image, lambda x: 255 - x)
            r2, g2, b2 = inverted_image.split()
            final_image = Image.merge('RGBA', (r2, g2, b2, a))
        else:
            final_image = Image.eval(image, lambda x: 255 - x)
            
        buffer = io.BytesIO()
        final_image.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.getvalue()
