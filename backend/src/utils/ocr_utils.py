from PIL import Image, ImageFilter
import pytesseract
import cv2
import os
import re
import csv

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


# clean_text function to remove unwanted characters
def clean_text(text):
    # Remove special characters and multiple whitespaces
    cleaned_text = re.sub(r'[^\w\s]', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()


def parse_text(text):
    # This is a simplistic parser and likely needs to be adjusted
    product_info_pattern = re.compile(r'(?P<name>.+?) - \$(?P<price>\d+(\.\d{2})?) - (?P<offer>.+)')
    products = []

    for line in text.split('\n'):
        match = product_info_pattern.match(line)
        if match:
            product_info = match.groupdict()
            product_info['price'] = float(product_info['price'])  # Convert price to float
            products.append(product_info)
    return products


def extract_text_from_image(image_path):
    try:
        preprocessed_path = preprocess_image(image_path)
        if preprocessed_path is None:
            return "Preprocessing failed."
        img = Image.open(preprocessed_path)
        raw_text = pytesseract.image_to_string(img)
        os.remove(preprocessed_path)
        # Save the extracted text to a CSV file
        # assing the path to the CSV file for me
        csv_file_path = os.path.join('data', 'extracted_text.csv')
        with open(csv_file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Each row in the CSV contains the image path and the associated text
            writer.writerow([image_path, raw_text])

        print(f"Processed {image_path}, text saved to {csv_file_path}")
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return None
