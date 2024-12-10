import sys
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from datetime import datetime

class ImplantDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = Image.open(image_path)
        self.draw = ImageDraw.Draw(self.image)
        
    def convert_to_grayscale(self):
        """Convert image to grayscale for better processing"""
        return self.image.convert('L')
    
    def detect_implants(self, threshold=200):
        """
        Detect implants using basic thresholding
        Returns list of detected implants with their coordinates
        """
        gray_image = self.convert_to_grayscale()
        np_image = np.array(gray_image)
        
        # Simple thresholding to detect high-density objects (implants)
        binary = np_image > threshold
        
        # Find connected components (potential implants)
        implants = []
        visited = np.zeros_like(binary)
        
        for y in range(binary.shape[0]):
            for x in range(binary.shape[1]):
                if binary[y, x] and not visited[y, x]:
                    # Found a new implant, flood fill to get its extent
                    implant = self._flood_fill(binary, visited, x, y)
                    if len(implant) > 100:  # Minimum size threshold
                        implants.append(implant)
        
        return implants
    
    def _flood_fill(self, binary, visited, start_x, start_y):
        """Helper method to find connected components"""
        stack = [(start_x, start_y)]
        points = []
        
        while stack:
            x, y = stack.pop()
            if (x < 0 or x >= binary.shape[1] or 
                y < 0 or y >= binary.shape[0] or 
                visited[y, x] or not binary[y, x]):
                continue
                
            visited[y, x] = True
            points.append((x, y))
            
            # Add neighbors
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
            
        return points
    
    def measure_implant(self, implant_points):
        """Calculate dimensions of detected implant"""
        x_coords = [p[0] for p in implant_points]
        y_coords = [p[1] for p in implant_points]
        
        # Calculate dimensions in pixels
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        
        # Estimate diameter (average of width and height)
        diameter = (width + height) / 2
        
        # Get center point
        center_x = sum(x_coords) / len(x_coords)
        center_y = sum(y_coords) / len(y_coords)
        
        return {
            'width': width,
            'height': height,
            'diameter': diameter,
            'center': (int(center_x), int(center_y))
        }
    
    def annotate_image(self, implants_data):
        """Draw measurements on the image"""
        try:
            font = ImageFont.load_default()
        except:
            font = None
            
        for i, implant in enumerate(implants_data, 1):
            center = implant['center']
            
            # Draw circle around implant
            radius = int(implant['diameter'] / 2)
            self.draw.ellipse(
                [
                    center[0] - radius, 
                    center[1] - radius,
                    center[0] + radius, 
                    center[1] + radius
                ],
                outline='red'
            )
            
            # Add measurements text
            text = f"Implant {i}:\nW: {implant['width']:.1f}px\nH: {implant['height']:.1f}px\nD: {implant['diameter']:.1f}px"
            self.draw.text(
                (center[0] + radius + 10, center[1] - radius),
                text,
                fill='red',
                font=font
            )
    
    def save_annotated_image(self):
        """Save the annotated image with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"annotated_xray_{timestamp}.png"
        self.image.save(output_path)
        return output_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python implant_detector.py <path_to_xray_image>")
        return
        
    image_path = sys.argv[1]
    
    try:
        detector = ImplantDetector(image_path)
        
        # Detect implants
        print("Detecting implants...")
        implants = detector.detect_implants()
        
        if not implants:
            print("No implants detected in the image.")
            return
            
        # Measure and collect data for each implant
        implants_data = []
        print("\nImplant Measurements:")
        print("-" * 50)
        
        for i, implant_points in enumerate(implants, 1):
            measurements = detector.measure_implant(implant_points)
            implants_data.append(measurements)
            
            print(f"\nImplant {i}:")
            print(f"Width: {measurements['width']:.1f} pixels")
            print(f"Height: {measurements['height']:.1f} pixels")
            print(f"Diameter: {measurements['diameter']:.1f} pixels")
            print(f"Center position: {measurements['center']}")
        
        # Annotate and save image
        detector.annotate_image(implants_data)
        output_path = detector.save_annotated_image()
        print(f"\nAnnotated image saved as: {output_path}")
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()