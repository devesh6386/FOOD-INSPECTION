def calculate_real_size(pixel_width, pixel_height, pixels_per_metric):
    if pixels_per_metric is None or pixels_per_metric == 0:
        return 0.0, 0.0
        
    real_width_mm = pixel_width / pixels_per_metric
    real_height_mm = pixel_height / pixels_per_metric
    
    return real_width_mm, real_height_mm