from django.db import models
from django.contrib.auth.models import User


class PDF(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pdfs')
    filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100, default='application/pdf')
    data = models.BinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    size = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.filename} ({self.user.username})"
  
