from django.db import models
import os
import uuid

class ProcessedImage(models.Model):
    """Model for tracking processed images and their metadata"""
    
    FILTER_CHOICES = [
        ('gray', 'Grayscale'),
        ('sepia', 'Sepia'),
        ('poster', 'Poster'),
        ('blur', 'Blur'),
        ('edge', 'Edge Detection'),
        ('solar', 'Solarize'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    original_image = models.CharField(max_length=255)  # Path to original image
    processed_image = models.CharField(max_length=255)  # Path to processed image
    original_filename = models.CharField(max_length=100)
    filter_applied = models.CharField(max_length=10, choices=FILTER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.original_filename} - {self.get_filter_applied_display()}"
    
    def delete(self, *args, **kwargs):
        # Delete the image files when the model instance is deleted
        try:
            if os.path.isfile(self.original_image):
                os.remove(self.original_image)
            if os.path.isfile(self.processed_image):
                os.remove(self.processed_image)
        except Exception as e:
            print(f"Error deleting files: {e}")
            
        super().delete(*args, **kwargs)
