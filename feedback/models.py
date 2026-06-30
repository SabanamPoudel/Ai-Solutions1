from django.db import models


class Feedback(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    rating = models.IntegerField(choices=RATING_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} — {self.rating}★"

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name_plural = 'Feedback'
