import os

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(BASE_DIR, "images")
OUTPUT_DIR = os.path.join(BASE_DIR, "labels")
CROPS_OUTPUT_DIR = os.path.join(BASE_DIR, "crops")

# --- YOLO CONFIGURATION ---
UNIFIED_CLASSES = [
    "BARCODE", "CONSUMER_CARE", "GENERIC_NAME", 
    "INFO_PANEL", "MANUFACTURER", "PRINCIPAL_DISPLAY_PANEL", "STAMP_PANEL"
]

CLASS_COLORS = {
    "BARCODE": (0, 255, 255),                
    "CONSUMER_CARE": (50, 205, 50),           
    "GENERIC_NAME": (30, 144, 255),           
    "INFO_PANEL": (255, 0, 255),              
    "MANUFACTURER": (255, 69, 0),             
    "PRINCIPAL_DISPLAY_PANEL": (255, 215, 0), 
    "STAMP_PANEL": (138, 43, 226)         
}

MODEL_CONFIGS = [
    {
        "weights": os.path.join(BASE_DIR, "models", "yolo26n-seg.pt"),
        "allowed_classes": ["CONSUMER_CARE","PRINCIPAL_DISPLAY_PANEL"]
    },
    {
        "weights": os.path.join(BASE_DIR, "models", "yolov8n.pt"),
        "allowed_classes": ["GENERIC_NAME"]
    },
    {
        "weights": os.path.join(BASE_DIR, "models", "yolov8n-seg.pt"),
        "allowed_classes": ["BARCODE","MANUFACTURER","STAMP_PANEL","INFO_PANEL"]
    }
]

CONFIDENCE = 0.25
SAVE_CROPS = False

# --- OCR & SCALING CONFIGURATION ---
OCR_LANGUAGES = ['en']
OCR_USE_GPU = True

# 10 Rupee coin diameter in mm
COIN_DIAMETER_MM = 27.0  

ROBOFLOW_WORKSPACE = "harishsingh"
ROBOFLOW_WORKFLOW_ID = "coin-location-detector"