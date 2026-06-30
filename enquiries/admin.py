from django.contrib import admin
from .models import Enquiry

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject', 'status', 'submitted_at']
    list_filter = ['status']
    search_fields = ['full_name', 'email', 'subject']
    list_editable = ['status']
    ordering = ['-submitted_at']
