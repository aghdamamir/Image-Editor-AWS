from django.urls import path
from . import views

app_name = 'processing'

urlpatterns = [
    path('', views.index, name='index'),
    path('process/', views.process_image_view, name='process_image'),
    path('result/<uuid:image_id>/', views.result_view, name='result'),
    path('download/<uuid:image_id>/', views.download_image, name='download'),
    path('gallery/', views.gallery_view, name='gallery'),
]
