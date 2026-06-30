from django import forms
from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['full_name', 'email', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'fullName',
                'placeholder': 'Your full name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'id': 'email',
                'placeholder': 'your@email.com',
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-input',
                'id': 'subject',
                'placeholder': 'e.g. Enquiry about Machine Learning Solutions',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-textarea',
                'id': 'enquiryMessage',
                'rows': 6,
                'placeholder': 'Describe your enquiry, the AI service you are interested in, or any questions about the platform...',
            }),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'subject': 'Subject',
            'message': 'Enquiry Message',
        }
