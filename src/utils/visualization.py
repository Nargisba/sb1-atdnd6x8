from PIL import ImageDraw, ImageFont
import math

def draw_measurement_line(draw, start, end, color='red', width=2):
    """Draw a measurement line with end caps"""
    # Draw the main line
    draw.line([start, end], fill=color, width=width)
    
    # Draw end caps (small perpendicular lines)
    cap_length = 10
    if start[0] == end[0]:  # Vertical line
        # Top cap
        draw.line([
            (start[0] - cap_length//2, start[1]),
            (start[0] + cap_length//2, start[1])
        ], fill=color, width=width)
        # Bottom cap
        draw.line([
            (end[0] - cap_length//2, end[1]),
            (end[0] + cap_length//2, end[1])
        ], fill=color, width=width)
    else:  # Horizontal line
        # Left cap
        draw.line([
            (start[0], start[1] - cap_length//2),
            (start[0], start[1] + cap_length//2)
        ], fill=color, width=width)
        # Right cap
        draw.line([
            (end[0], end[1] - cap_length//2),
            (end[0], end[1] + cap_length//2)
        ], fill=color, width=width)

def draw_implant_annotation(draw, implant_data, implant_number, font=None):
    """Draw annotation for a single implant with measurement lines"""
    center = implant_data['center']
    width = implant_data['width']
    height = implant_data['height']
    diameter = implant_data['diameter']
    
    # Calculate bounding box coordinates
    left = center[0] - width//2
    right = center[0] + width//2
    top = center[1] - height//2
    bottom = center[1] + height//2
    
    # Draw outline
    draw.rectangle([left, top, right, bottom], outline='lime', width=2)
    
    # Draw measurement lines
    # Height line (vertical)
    height_start = (center[0] + width//2 + 20, top)
    height_end = (center[0] + width//2 + 20, bottom)
    draw_measurement_line(draw, height_start, height_end, 'cyan')
    
    # Width line (horizontal)
    width_start = (left, top - 20)
    width_end = (right, top - 20)
    draw_measurement_line(draw, width_start, width_end, 'cyan')
    
    # Diameter line (diagonal)
    diagonal_start = (left, top)
    diagonal_end = (right, bottom)
    draw_measurement_line(draw, diagonal_start, diagonal_end, 'yellow')
    
    # Add measurements text with better positioning
    if font is None:
        try:
            font = ImageFont.load_default()
        except:
            pass
    
    # Position text for measurements
    text_color = 'cyan'
    # Height text
    height_text = f"Height: {height:.1f}px"
    draw.text(
        (center[0] + width//2 + 25, center[1] - 10),
        height_text,
        fill=text_color,
        font=font
    )
    
    # Width text
    width_text = f"Width: {width:.1f}px"
    draw.text(
        (center[0] - 20, top - 35),
        width_text,
        fill=text_color,
        font=font
    )
    
    # Diameter text
    dia_text = f"Dia: {diameter:.1f}px"
    draw.text(
        (center[0] - width//4, center[1] - height//4),
        dia_text,
        fill='yellow',
        font=font
    )
    
    # Draw implant number
    draw.text(
        (left - 30, top),
        f"Implant {implant_number}",
        fill='white',
        font=font
    )