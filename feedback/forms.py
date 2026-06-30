from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['full_name', 'email', 'rating', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'id': 'feedbackName',
                'placeholder': 'Enter your full name',
                'required': True,
                'style': 'width:100%; padding:12px 16px; border-radius:8px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-primary); font-family:inherit; font-size:14px; box-sizing:border-box;',
            }),
            'email': forms.EmailInput(attrs={
                'id': 'feedbackEmail',
                'placeholder': 'your@email.com',
                'required': True,
                'style': 'width:100%; padding:12px 16px; border-radius:8px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-primary); font-family:inherit; font-size:14px; box-sizing:border-box;',
            }),
            'rating': forms.Select(attrs={
                'id': 'feedbackRating',
                'required': True,
                'style': 'width:100%; padding:12px 16px; border-radius:8px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-primary); font-family:inherit; font-size:14px; box-sizing:border-box;',
            }),
            'message': forms.Textarea(attrs={
                'id': 'feedbackMessage',
                'rows': 5,
                'placeholder': 'Share your experience with the platform, services, content, or navigation...',
                'required': True,
                'style': 'width:100%; padding:12px 16px; border-radius:8px; border:1px solid var(--border); background:var(--bg-card); color:var(--text-primary); font-family:inherit; font-size:14px; box-sizing:border-box; resize:vertical;',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'rating': 'Rating (1–5)',
            'message': 'Feedback Message',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].choices = [
            ('', 'Select a rating'),
            (5, '★★★★★ — Excellent'),
            (4, '★★★★☆ — Good'),
            (3, '★★★☆☆ — Average'),
            (2, '★★☆☆☆ — Below Average'),
            (1, '★☆☆☆☆ — Poor'),
        ]
