from PIL import Image
import pytesseract
import os

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def extract_text_from_image(image_path):
    """
    Uses pytesseract to extract text from an image.

    :param image_path: Path to the image file.
    :return: Extracted text as a string.
    """
    try:
        text = pytesseract.image_to_string(Image.open(image_path))
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None


