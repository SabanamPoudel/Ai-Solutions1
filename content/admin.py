from django.contrib import admin
from .models import AIService, Article, Event, EventImage, ChatbotResponse


class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 1

@admin.register(AIService)
class AIServiceAdmin(admin.ModelAdmin):
    list_display = ['icon', 'title', 'is_active']
    list_editable = ['is_active']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'status', 'created_at']
    list_editable = ['status']
    list_filter = ['status', 'category']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'event_date', 'location', 'is_upcoming']
    list_editable = ['is_upcoming']
    list_filter = ['event_type', 'is_upcoming']
    ordering = ['event_date']
    inlines = [EventImageInline]

@admin.register(ChatbotResponse)
class ChatbotResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'is_active', 'updated_at']
    list_editable = ['is_active']
