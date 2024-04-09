from PIL import Image, ImageFilter
import pytesseract
import cv2
import os

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
  try:

    # Convert to grayscale
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Gaussian blur
    image = cv2.GaussianBlur(image, (5, 5), 0)

    # Apply thresholding
    _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Save or return preprocessed image
    preprocessed_path = 'preprocessed_' + os.path.basename(image_path)
    cv2.imwrite(preprocessed_path, image)
    return preprocessed_path
  except Exception as e:
    print(f"Error processing {image_path}: {str(e)}")
    return None

def extract_text_from_image(image_path):
    """
    Uses pytesseract to extract text from an image.

    :param image_path: Path to the image file.
    :return: Extracted text as a string.
    """
    try:
        # Preprocess the image to enhance OCR accuracy
        preprocessed_path = preprocess_image(image_path)
        if preprocessed_path is None:
            return "Preprocessing failed."
        # Load the preprocessed image with PIL
        img = Image.open(preprocessed_path)
        # Use Tesseract to do OCR on the image
        text = pytesseract.image_to_string(img)
        # Clean up: remove the preprocessed image file
        os.remove(preprocessed_path)
        return text
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None


