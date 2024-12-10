from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime
from utils.image_processing import convert_to_grayscale
from utils.measurements import calculate_implant_dimensions
from utils.visualization import draw_implant_annotation
from utils.implant_detection import detect_metal_objects, filter_implant_candidates
from utils.calibration import XrayCalibrator

class ImplantDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        self.calibrator = XrayCalibrator()
        
    def detect_implants(self, threshold=200):
        """Detect implants using advanced filtering"""
        gray_image = convert_to_grayscale(self.image)
        np_image = np.array(gray_image)
        
        # Detect metal objects
        labeled_array, num_features = detect_metal_objects(np_image, threshold)
        
        # Filter for implant-like objects
        implants = filter_implant_candidates(labeled_array)
        
        return implants
    
    def measure_implants(self, implants):
        """Measure implants and convert to millimeters"""
        measurements = []
        
        for implant_points in implants:
            pixels_measurements = calculate_implant_dimensions(implant_points)
            
            # Convert measurements to millimeters
            mm_measurements = {
                'width': self.calibrator.pixels_to_mm(pixels_measurements['width']),
                'height': self.calibrator.pixels_to_mm(pixels_measurements['height']),
                'diameter': self.calibrator.pixels_to_mm(pixels_measurements['diameter']),
                'center': pixels_measurements['center'],  # Keep center in pixels for drawing
                'pixels': pixels_measurements  # Keep pixel measurements for reference
            }
            
            measurements.append(mm_measurements)
            
        return measurements
    
    def annotate_image(self, implants_data):
        """Draw measurements on the image"""
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        for i, implant in enumerate(implants_data, 1):
            draw_implant_annotation(self.draw, implant, i, font)
    
    def save_annotated_image(self):
        """Save the annotated image with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"annotated_xray_{timestamp}.png"
        self.image.save(output_path)
        return output_path