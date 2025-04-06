"""
Utility functions for image processing using Pillow
"""
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import os
import uuid
from django.conf import settings

def save_uploaded_image(uploaded_file):
    """
    Save the uploaded image to the filesystem
    
    Args:
        uploaded_file: InMemoryUploadedFile from form
        
    Returns:
        tuple: (filename, filepath)
    """
    # Generate a unique filename
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    unique_filename = f"{uuid.uuid4()}{ext}"
    
    # Define the path where the file will be saved
    filepath = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Save the file
    with open(filepath, 'wb+') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    
    return unique_filename, filepath

def apply_grayscale(image_path, output_path):
    """Convert image to grayscale"""
    with Image.open(image_path) as img:
        grayscale_img = img.convert('L')
        grayscale_img.save(output_path)
    return output_path

def apply_sepia(image_path, output_path):
    """Apply sepia tone effect"""
    with Image.open(image_path) as img:
        # Convert to grayscale first
        grayscale = img.convert('L')
        # Create a sepia palette
        sepia = Image.new('RGB', img.size, (0, 0, 0))
        for y in range(img.height):
            for x in range(img.width):
                gray_pixel = grayscale.getpixel((x, y))
                # Apply sepia tone formula
                r = min(int(gray_pixel * 1.1), 255)
                g = min(int(gray_pixel * 0.9), 255)
                b = min(int(gray_pixel * 0.7), 255)
                sepia.putpixel((x, y), (r, g, b))
        sepia.save(output_path)
    return output_path

def apply_poster(image_path, output_path):
    """Apply posterize effect"""
    with Image.open(image_path) as img:
        # Posterize (reduce number of colors)
        posterized = ImageOps.posterize(img.convert('RGB'), 3)
        posterized.save(output_path)
    return output_path

def apply_blur(image_path, output_path):
    """Apply blur effect"""
    with Image.open(image_path) as img:
        # Apply Gaussian blur
        blurred = img.filter(ImageFilter.GaussianBlur(radius=3))
        blurred.save(output_path)
    return output_path

def apply_edge(image_path, output_path):
    """Apply edge detection"""
    with Image.open(image_path) as img:
        # Convert to grayscale and apply edge filter
        edges = img.convert('L').filter(ImageFilter.FIND_EDGES)
        edges.save(output_path)
    return output_path

def apply_solar(image_path, output_path):
    """Apply solarize effect"""
    with Image.open(image_path) as img:
        # Solarize (invert all pixel values above a threshold)
        solarized = ImageOps.solarize(img.convert('RGB'), threshold=128)
        solarized.save(output_path)
    return output_path

def process_image(image_path, filter_type):
    """
    Process an image with the specified filter
    
    Args:
        image_path: Path to the input image
        filter_type: Type of filter to apply
        
    Returns:
        str: Path to the processed image
    """
    # Generate output filename with filter type as suffix
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_filename = f"{name}_{filter_type}{ext}"
    output_path = os.path.join(settings.PROCESSED_DIR, output_filename)
    
    # Apply the selected filter
    filter_functions = {
        'gray': apply_grayscale,
        'sepia': apply_sepia,
        'poster': apply_poster,
        'blur': apply_blur,
        'edge': apply_edge,
        'solar': apply_solar
    }
    
    if filter_type in filter_functions:
        return filter_functions[filter_type](image_path, output_path)
    else:
        raise ValueError(f"Unknown filter type: {filter_type}")
