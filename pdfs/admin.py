from django.contrib import admin
from .models import PDF


@admin.register(PDF)
class PDFAdmin(admin.ModelAdmin):
    list_display = ('filename', 'user', 'size', 'uploaded_at')
    search_fields = ('filename', 'user__username')
    readonly_fields = ('uploaded_at',)
