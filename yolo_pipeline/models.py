import json
import copy
from pathlib import Path
from datetime import datetime
import cv2
from ultralytics import YOLO

from config import UNIFIED_CLASSES

def extract_detections(result, image_path: Path, crops_dir: Path | None, start_det_id: int, allowed_classes: list):
    img = cv2.imread(str(image_path))
    img_h, img_w = result.orig_shape

    class_names = result.names
    boxes = result.boxes
    masks = result.masks

    detections = []
    current_det_id = start_det_id
    
    for i in range(len(boxes)):
        cls_id = int(boxes.cls[i])
        cls_name = class_names[cls_id]
        
        if cls_name not in allowed_classes:
            continue

        conf = float(boxes.conf[i])
        x1, y1, x2, y2 = [float(v) for v in boxes.xyxy[i]]
        xc, yc, w, h = [float(v) for v in boxes.xywhn[i]]

        detection = {
            "detection_id": current_det_id,
            "class_name": cls_name,
            "class_id": UNIFIED_CLASSES.index(cls_name) if cls_name in UNIFIED_CLASSES else cls_id,
            "confidence": round(conf, 4),
            "bbox_pixels": {
                "x_min": round(x1, 1), "y_min": round(y1, 1),
                "x_max": round(x2, 1), "y_max": round(y2, 1),
            },
            "bbox_normalized": {
                "x_center": round(xc, 5), "y_center": round(yc, 5),
                "width": round(w, 5), "height": round(h, 5),
            },
            "polygon_pixels": None,
            "crop_path": None,
        }

        if masks is not None:
            polygon = masks.xy[i]
            detection["polygon_pixels"] = [[round(float(px), 1), round(float(py), 1)] for px, py in polygon]

        if crops_dir is not None and img is not None:
            crops_dir.mkdir(parents=True, exist_ok=True)
            xi1, yi1 = max(0, int(x1)), max(0, int(y1))
            xi2, yi2 = min(img_w, int(x2)), min(img_h, int(y2))
            crop = img[yi1:yi2, xi1:xi2]

            if crop.size > 0:
                crop_name = f"{image_path.stem}_{cls_name}_{current_det_id}.jpg"
                crop_path = crops_dir / crop_name
                cv2.imwrite(str(crop_path), crop)
                detection["crop_path"] = str(crop_path)

        detections.append(detection)
        current_det_id += 1

    return detections, img_w, img_h


def run_delegated_models(model_configs: list, source: str, output_dir: str, crops_out_dir: str, conf: float, save_crops: bool):
    #for image in images:
        # Just add device="mps" to the existing predict call here:
    #  results = model.predict(source=image, conf=conf, save_crop=save_crops, device="mps")
    loaded_models = []
    for config in model_configs:
        model = YOLO(config["weights"])
        loaded_models.append({
            "model": model,
            "weights": config["weights"],
            "task": model.task,
            "allowed_classes": config["allowed_classes"]
        })
    
    source_path = Path(source)
    if source_path.is_dir():
        image_paths = sorted([p for p in source_path.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".webp")])

        #image_paths = sorted([p for p in source_path.iterdir() if p.suffix.lower() in (".jpg", ".jpeg", ".png")])
    else:
        image_paths = [source_path]

    if not image_paths:
        raise FileNotFoundError(f"No images found at {source}")

    crops_dir = Path(crops_out_dir) if save_crops else None
    out_dir_path = Path(output_dir)
    out_dir_path.mkdir(parents=True, exist_ok=True)

    generated_json_paths = [] 

    for img_path in image_paths:
        img_detections = []
        img_w, img_h = 0, 0
        
        for m_data in loaded_models:
            results = m_data["model"].predict(source=str(img_path), conf=conf, verbose=False)
            start_id = len(img_detections)
            new_dets, w, h = extract_detections(
                result=results[0], 
                image_path=img_path, 
                crops_dir=crops_dir, 
                start_det_id=start_id,
                allowed_classes=m_data["allowed_classes"]
            )
            img_detections.extend(new_dets)
            img_w, img_h = w, h 
            
        output_payload = {
            "ensemble_configuration": [
                {"weights": m["weights"], "task": m["task"], "allowed_classes": m["allowed_classes"]} 
                for m in loaded_models
            ],
            "confidence_threshold": conf,
            "generated_on": datetime.now().isoformat(timespec="seconds"),
            "image_file": img_path.name,
            "image_width": img_w,
            "image_height": img_h,
            "num_detections": len(img_detections),
            "detections": img_detections,
        }

        seg_json_path = out_dir_path / f"{img_path.stem}_seg.json"
        with open(seg_json_path, "w") as f:
            json.dump(output_payload, f, indent=2)
            
        generated_json_paths.append(str(seg_json_path))

        box_payload = copy.deepcopy(output_payload)
        for det in box_payload["detections"]:
            det["polygon_pixels"] = None 

        box_json_path = out_dir_path / f"{img_path.stem}_box.json"
        with open(box_json_path, "w") as f:
            json.dump(box_payload, f, indent=2)
    return generated_json_paths