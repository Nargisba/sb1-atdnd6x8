from PIL import Image
import numpy as np

def convert_to_grayscale(image):
    """Convert image to grayscale for better processing"""
    return image.convert('L')

def flood_fill(binary, visited, start_x, start_y):
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

def threshold_image(np_image, threshold=200):
    """Apply thresholding to identify high-density objects"""
    return np_image > threshold