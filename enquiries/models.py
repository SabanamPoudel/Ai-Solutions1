from django.db import models


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Under Review', 'Under Review'),
        ('Responded', 'Responded'),
        ('Closed', 'Closed'),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.full_name} — {self.subject}"

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Enquiries'
