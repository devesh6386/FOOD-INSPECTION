import os
from inference_sdk import InferenceHTTPClient, InferenceConfiguration
from dotenv import load_dotenv
import config
load_dotenv()

client = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key=os.getenv("ROBOFLOW_API_KEY")
).configure(InferenceConfiguration(
    api_key_transport="header" 
))

def calculate_pixels_per_metric(image_path):
    """
    Detects a reference coin using a Roboflow Workflow
    and returns the pixels-per-mm ratio.
    """
    try:
        result = client.run_workflow(
            workspace_name=config.ROBOFLOW_WORKSPACE,
            workflow_id=config.ROBOFLOW_WORKFLOW_ID,
            images={
                "image": image_path
            },
            parameters={
                "confidence": 0.4,
                "iou_threshold": 0.3,
                "class_agnostic_nms": False,
                "max_detections": 1
            },
            use_cache=True 
        )
        if isinstance(result, list) and len(result) > 0:
            image_result = result[0]
        else:
            image_result = result

        predictions = []

        for key, value in image_result.items():
            if isinstance(value, dict) and "predictions" in value:
                predictions = value["predictions"]
                break
            elif isinstance(value, list) and len(value) > 0 and "width" in value[0]:
                predictions = value
                break
            elif key == "predictions":
                predictions = value
                break

        if not predictions:
            print(f"No coin found in {os.path.basename(image_path)}.")
            return None
            
        best_prediction = sorted(predictions, key=lambda x: x['confidence'], reverse=True)[0]
        
        coin_pixel_width = best_prediction["width"]
        coin_pixel_height = best_prediction["height"]
        
        coin_pixel_diameter = max(coin_pixel_width, coin_pixel_height)
        
        pixels_per_metric = coin_pixel_diameter / config.COIN_DIAMETER_MM
        
        print(f"Coin detected! Scale: {pixels_per_metric:.2f} px/mm (Conf: {best_prediction['confidence']:.2f})")
        return pixels_per_metric
        
    except Exception as e:
        print(f"  [Error] Failed to connect to Roboflow workflow or process image: {e}")
        return None