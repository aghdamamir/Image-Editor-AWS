"""
Storage utilities for handling images
"""
import os
from django.conf import settings
from .models import ProcessedImage

def save_processed_image_record(original_filename, original_path, processed_path, filter_type):
    """
    Save a record of processed image to database
    
    Args:
        original_filename: Original filename
        original_path: Path to original image
        processed_path: Path to processed image
        filter_type: Filter applied to the image
        
    Returns:
        ProcessedImage: The created record
    """
    # Create a new ProcessedImage instance
    image_record = ProcessedImage(
        original_image=original_path,
        processed_image=processed_path,
        original_filename=original_filename,
        filter_applied=filter_type
    )
    image_record.save()
    
    return image_record

def get_relative_path(absolute_path):
    """
    Convert absolute file path to relative path for URL construction
    
    Args:
        absolute_path: Absolute path to file
        
    Returns:
        str: Relative path
    """
    if absolute_path.startswith(settings.MEDIA_ROOT):
        return absolute_path[len(settings.MEDIA_ROOT):].lstrip('/')
    return absolute_path
