from django.contrib import admin
from .models import Feedback

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'rating', 'status', 'submitted_at']
    list_filter = ['status', 'rating']
    search_fields = ['full_name', 'email']
    list_editable = ['status']
    ordering = ['-submitted_at']
