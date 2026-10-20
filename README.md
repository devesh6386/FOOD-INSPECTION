# LabelGuard

An automated compliance verification platform for packaged commodity labels under India's Legal Metrology Act and Packaged Commodities Rules.

## Overview

LabelGuard helps regulatory inspectors and administrators verify packaged product labels quickly and accurately. In traditional workflows, legal metrology inspectors manually check packaging for required declarations such as MRP, net quantity, manufacturer details, and date markings. LabelGuard automates this process by analyzing package photos with computer vision and optical character recognition, measuring text dimensions against reference objects, and checking compliance against regulatory standards.

## Features

- **Multi-Model Label Detection**: Uses an ensemble of YOLO models to locate mandatory panels including barcodes, principal display panels, manufacturer details, and consumer care blocks.
- **Text Extraction and OCR**: Extracts printed text from detected regions using EasyOCR.
- **Physical Scale Calibration**: Computes a pixel-to-millimeter ratio using a reference coin detected through Roboflow workflows to evaluate real-world font height.
- **Compliance Reporting**: Flags missing mandatory declarations and undersized text declarations.
- **Role-Based Portals**: Provides dedicated web interfaces and API access for Inspectors and Administrators.
- **Evidence Archival**: Stores structured inspection records in MongoDB Atlas and uploads evidence images to Cloudinary.

## Tech Stack

- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **Database & Storage**: MongoDB Atlas (Motor async driver), Cloudinary
- **Authentication**: JWT (python-jose), bcrypt password hashing (passlib)
- **Computer Vision & OCR**: Ultralytics YOLO (detection and segmentation), EasyOCR, OpenCV, NumPy
- **Spatial Calibration**: Roboflow Inference SDK
- **Frontend**: Vanilla HTML5, CSS3, JavaScript

## Installation and Setup

### Prerequisites

- Python 3.10 or higher
- A MongoDB Atlas instance or local MongoDB server
- Cloudinary account credentials
- Roboflow account with workflow access

### Setup Steps

1. Clone the repository and navigate into the project directory:

```bash
git clone https://github.com/devesh6386/FOOD-INSPECTION.git
cd "labelguard auth"
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required Python packages:

```bash
pip install -r requirements.txt
```

4. Create and configure your environment file:

```bash
cp .env.example .env
```

Populate the `.env` file with the required credentials outlined below.

5. Seed initial admin and inspector accounts:

```bash
python seed.py
```

## Environment Variables

Configure the following keys in your `.env` file:

- `MONGO_URI`: MongoDB connection string.
- `CLOUDINARY_CLOUD_NAME`: Cloudinary account cloud name.
- `CLOUDINARY_API_KEY`: Cloudinary API public key.
- `CLOUDINARY_API_SECRET`: Cloudinary API secret key.
- `ROBOFLOW_API_KEY`: Roboflow serverless inference API key.
- `ROBOFLOW_WORKSPACE`: Roboflow workspace identifier.
- `ROBOFLOW_WORKFLOW_ID`: Roboflow coin-detection workflow ID.
- `ALGORITHM`: JWT signing algorithm (e.g., `HS256`).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token lifetime in minutes (e.g., `30`).

## Usage

1. Start the FastAPI development server:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. Open `http://localhost:8000` in your web browser.
3. Sign in using seeded credentials (such as inspector `OFC-7491` with password `inspectorpass` or admin `ADM-9002` with password `adminpass123`).
4. To run an inspection, upload product images on the Inspector Dashboard or send a multipart `POST` request to `/api/analyze-scan`.
5. Review the resulting JSON report for detected label regions, extracted text fields, physical font dimensions, and compliance status.

## Project Structure

```
labelguard-auth/
├── main.py                     # FastAPI application setup and API routing
├── database.py                 # Async MongoDB connection with Motor
├── security.py                 # Password hashing and JWT generation
├── dependencies.py             # Authentication and role verification
├── schemas.py                  # Pydantic request and response schemas
├── seed.py                     # Initial database seeding script
├── index.html                  # User login interface
├── inspector_dashboard.html    # Inspector portal interface
├── admin_dashboard.html        # Administrator dashboard interface
├── script.js                   # Client-side authentication and API interaction
├── style.css                   # Interface styling
├── yolo_pipeline/              # AI inspection pipeline
│   ├── config.py               # Model configurations and label classes
│   ├── pipeline_entry.py       # Detection and measurement orchestrator
│   ├── models.py               # YOLO model loading and inference
│   ├── masking.py              # OpenCV region-of-interest extraction
│   ├── ocr.py                  # EasyOCR text extraction
│   ├── scaling.py              # Reference coin detection via Roboflow
│   ├── measurement.py          # Metric conversions (pixels to millimeters)
│   └── models/                 # Pretrained YOLO model weights
└── requirements.txt            # Project dependencies
```

## Future Improvements

- Add asynchronous background worker queues (such as Celery or Redis) for high-volume batch processing.
- Integrate large language models to validate nutritional panels and ingredient claims.
- Extend OCR support for multilingual label declarations across regional scripts.
- Implement automated officer account approval workflows in the administrator panel.
