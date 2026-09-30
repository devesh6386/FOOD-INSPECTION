import cv2
import numpy as np

def generate_masked_roi(image_path, yolo_detections, target_class_name):
    """
    Applies a polygon mask to isolate the text, turns the background white,
    and CROPS the image to save OCR processing time.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Could not read image: {image_path}")

    mask = np.zeros(image.shape[:2], dtype=np.uint8)
    found_target = False
    target_bbox = None

    for detection in yolo_detections:
        if detection.get("class_name") == target_class_name:
            found_target = True
            target_bbox = detection.get("bbox_pixels")

            poly_pixels = detection.get("polygon_pixels")
            if poly_pixels is not None:
                polygon_points = np.array(poly_pixels, dtype=np.int32).reshape((-1, 1, 2))
                cv2.fillPoly(mask, [polygon_points], 255)
            else:
                x1, y1 = int(target_bbox["x_min"]), int(target_bbox["y_min"])
                x2, y2 = int(target_bbox["x_max"]), int(target_bbox["y_max"])
                cv2.rectangle(mask, (x1, y1), (x2, y2), 255, -1)
            
            break 

    if not found_target:
        return None

    masked_image = cv2.bitwise_and(image, image, mask=mask)
    white_background = np.ones_like(image, dtype=np.uint8) * 255
    inverse_mask = cv2.bitwise_not(mask)
    background = cv2.bitwise_and(white_background, white_background, mask=inverse_mask)
    final_img = cv2.add(masked_image, background)
    
    x1, y1 = int(target_bbox["x_min"]), int(target_bbox["y_min"])
    x2, y2 = int(target_bbox["x_max"]), int(target_bbox["y_max"])
    
    img_h, img_w = final_img.shape[:2]
    x1 = max(0, x1 - 15)
    y1 = max(0, y1 - 15)
    x2 = min(img_w, x2 + 15)
    y2 = min(img_h, y2 + 15)
    
    cropped_img = final_img[y1:y2, x1:x2]

    return cropped_img