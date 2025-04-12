from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
import mimetypes

from .forms import ImageUploadForm
from .utils import save_uploaded_image, process_image
from .storage import save_processed_image_record, get_relative_path
from .models import ProcessedImage

def index(request):
    """Home page with image upload form"""
    form = ImageUploadForm()
    return render(request, 'processing/index.html', {'form': form})

def process_image_view(request):
    """Process uploaded image with selected filter"""
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded image
            original_filename = request.FILES['image'].name
            saved_filename, saved_filepath = save_uploaded_image(request.FILES['image'])
            
            # Process the image with selected filter
            filter_type = form.cleaned_data['filter_type']
            processed_filepath = process_image(saved_filepath, filter_type)
            
            # Save record to database
            image_record = save_processed_image_record(
                original_filename, 
                saved_filepath, 
                processed_filepath, 
                filter_type
            )
            
            # Redirect to result page
            return redirect(reverse('processing:result', kwargs={'image_id': image_record.id}))
        
    else:
        form = ImageUploadForm()
    
    return render(request, 'processing/index.html', {'form': form})

def result_view(request, image_id):
    """Display processed image result"""
    image_record = get_object_or_404(ProcessedImage, id=image_id)
    
    # Get the relative paths for use in templates
    original_url = os.path.join(settings.MEDIA_URL, get_relative_path(image_record.original_image))
    processed_url = os.path.join(settings.MEDIA_URL, get_relative_path(image_record.processed_image))
    
    context = {
        'image': image_record,
        'original_url': original_url,
        'processed_url': processed_url,
        'filter_name': image_record.get_filter_applied_display()
    }
    
    return render(request, 'processing/result.html', context)

def gallery_view(request):
    """Display a gallery of all processed images"""
    # Get all processed images ordered by creation date (newest first)
    all_images = ProcessedImage.objects.all().order_by('-created_at')
    
    # Setup pagination
    paginator = Paginator(all_images, 12)  # Show 12 images per page
    page = request.GET.get('page', 1)
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        images = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        images = paginator.page(paginator.num_pages)
    
    # Prepare image URLs for the template
    gallery_items = []
    for img in images:
        processed_url = os.path.join(settings.MEDIA_URL, get_relative_path(img.processed_image))
        original_url = os.path.join(settings.MEDIA_URL, get_relative_path(img.original_image))
        
        gallery_items.append({
            'id': img.id,
            'processed_url': processed_url,
            'original_url': original_url,
            'filter_name': img.get_filter_applied_display(),
            'original_filename': img.original_filename,
            'created_at': img.created_at
        })
    
    context = {
        'gallery_items': gallery_items,
        'images': images,  # For pagination
    }
    
    return render(request, 'processing/gallery.html', context)

def download_image(request, image_id):
    """Download the processed image"""
    image_record = get_object_or_404(ProcessedImage, id=image_id)
    
    # Check if file exists
    if not os.path.exists(image_record.processed_image):
        raise Http404("Image file does not exist")
    
    # Get the file name and content type
    filename = os.path.basename(image_record.processed_image)
    content_type, _ = mimetypes.guess_type(filename)
    
    # Read the file and serve it
    with open(image_record.processed_image, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
