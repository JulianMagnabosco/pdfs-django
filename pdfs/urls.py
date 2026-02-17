from django.urls import path
from . import views

urlpatterns = [
    path('', views.pdf_list, name='pdf_list'),
    path('upload/', views.upload_pdf, name='upload'),
    path('download/<int:pk>/', views.download_pdf, name='download'),
    path('register/', views.register, name='register'),
]
