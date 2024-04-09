import os
from fastapi import APIRouter, HTTPException, File, UploadFile
from typing import List
from utils.ocr_utils import extract_text_from_image

router = APIRouter(prefix="/flyers", tags=["flyers"])

@router.get("/", response_model=List[str])
async def get_flyers():
    """
    Get a list of all flyers available in the system
    """

    flyers_dir = "static/images/flyers"
    processed_texts = []

     # Ensure the directory exists
    if not os.path.exists(flyers_dir):
        raise HTTPException(status_code=404, detail="Flyers directory not found")


    for flyer in os.listdir(flyers_dir):
        flyer_path = os.path.join(flyers_dir, flyer)
        # Check if it's a file before processing
        if os.path.isfile(flyer_path):
            text = extract_text_from_image(flyer_path)
            if text:
                processed_texts.append(text)

    return processed_texts