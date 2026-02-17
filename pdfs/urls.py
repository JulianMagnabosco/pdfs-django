from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.RegisterView.as_view(), name='register'),
    path('api/login/', views.LoginView.as_view(), name='login'),
    path('api/pdfs/', views.PDFListView.as_view(), name='pdf_list'),
    path('api/pdfs/upload/', views.PDFUploadView.as_view(), name='pdf_upload'),
    path('api/pdfs/<int:pk>/', views.PDFDetailView.as_view(), name='pdf_detail'),
    path('api/pdfs/<int:pk>/download/', views.PDFDownloadView.as_view(), name='pdf_download'),
]
