from django.db import models


class AIService(models.Model):
    icon = models.CharField(max_length=10, default='🤖')
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.FileField(upload_to='content/services/', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]
    title = models.CharField(max_length=300)
    category = models.CharField(max_length=100, default='General')
    excerpt = models.TextField()
    content = models.TextField(blank=True)
    image = models.FileField(upload_to='content/articles/', blank=True)
    image_url = models.URLField(blank=True, default='')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='published')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Event(models.Model):
    EVENT_TYPES = [
        ('Conference', 'Conference'),
        ('Workshop', 'Workshop'),
        ('Webinar', 'Webinar'),
        ('Symposium', 'Symposium'),
        ('Seminar', 'Seminar'),
    ]
    title = models.CharField(max_length=300)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES, default='Workshop')
    event_date = models.DateField()
    location = models.CharField(max_length=300)
    description = models.TextField()
    image = models.FileField(upload_to='content/events/', blank=True)
    is_upcoming = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['event_date']


class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='gallery_images', on_delete=models.CASCADE)
    image = models.FileField(upload_to='content/events/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.caption or f'Image for {self.event.title}'

    class Meta:
        ordering = ['id']


class ChatbotResponse(models.Model):
    question = models.CharField(max_length=500)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question[:80]

    class Meta:
        ordering = ['display_order', 'question']
