from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError

class ImageUploadForm(forms.Form):
    """Form for uploading images and selecting filters"""
    
    FILTER_CHOICES = [
        ('gray', 'Grayscale'),
        ('sepia', 'Sepia'),
        ('poster', 'Poster'),
        ('blur', 'Blur'),
        ('edge', 'Edge Detection'),
        ('solar', 'Solarize'),
    ]
    
    image = forms.ImageField(
        label='Select an image',
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'})
    )
    
    filter_type = forms.ChoiceField(
        choices=FILTER_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        
        if image:
            # Check file size
            if image.size > settings.MAX_UPLOAD_SIZE:
                max_size_mb = settings.MAX_UPLOAD_SIZE / (1024 * 1024)
                raise ValidationError(f'Image file too large. Maximum size is {max_size_mb}MB.')
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            
            if ext not in valid_extensions:
                raise ValidationError(f'Unsupported file type. Please use: {", ".join(valid_extensions)}')
                
        return image
