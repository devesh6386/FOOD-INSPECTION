import easyocr
import numpy as np
import config


import torch
import easyocr

# Check for Apple Silicon GPU
use_gpu = torch.backends.mps.is_available()

# Initialize the reader with GPU enabled
reader = easyocr.Reader(['en'], gpu=use_gpu)
reader = easyocr.Reader(config.OCR_LANGUAGES, gpu=config.OCR_USE_GPU) 

def extract_and_measure_text(ocr_ready_image):
    results = reader.readtext(ocr_ready_image)
    
    extracted_data = []
    for (bbox, text, prob) in results:
        (tl, tr, br, bl) = bbox
        
        pixel_width = int(np.linalg.norm(np.array(tl) - np.array(tr)))
        pixel_height = int(np.linalg.norm(np.array(tl) - np.array(bl)))
        
        extracted_data.append({
            "text": text,
            "confidence": prob,
            "pixel_width": pixel_width,
            "pixel_height": pixel_height
        })
        
    return extracted_data