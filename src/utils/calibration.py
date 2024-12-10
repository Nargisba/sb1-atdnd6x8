"""Utilities for pixel to millimeter conversion and calibration"""

class XrayCalibrator:
    # Standard dental implant sizes range from 8mm to 16mm in length
    # We'll use this for automatic calibration
    STANDARD_IMPLANT_LENGTH_MM = 12  # typical implant length
    
    def __init__(self, image_resolution_dpi=300):
        # Standard X-ray resolution is typically 300 DPI
        self.dpi = image_resolution_dpi
        self.mm_per_pixel = 25.4 / self.dpi  # 25.4mm = 1 inch
        
    def pixels_to_mm(self, pixels):
        """Convert pixels to millimeters"""
        return pixels * self.mm_per_pixel
        
    def mm_to_pixels(self, mm):
        """Convert millimeters to pixels"""
        return mm / self.mm_per_pixel