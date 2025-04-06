from django.contrib import admin
from .models import ProcessedImage

@admin.register(ProcessedImage)
class ProcessedImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_filename', 'filter_applied', 'created_at')
    list_filter = ('filter_applied', 'created_at')
    search_fields = ('original_filename',)
