def calculate_implant_dimensions(implant_points):
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

def format_measurements(measurements, implant_number):
    """Format measurements for display"""
    return (
        f"Implant {implant_number}:\n"
        f"Width: {measurements['width']:.1f} pixels\n"
        f"Height: {measurements['height']:.1f} pixels\n"
        f"Diameter: {measurements['diameter']:.1f} pixels\n"
        f"Center position: {measurements['center']}"
    )