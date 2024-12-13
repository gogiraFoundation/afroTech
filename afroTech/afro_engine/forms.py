from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    """
    Represents a contact form submission.
    """
    class Meta:
        model = Contact  # Use the correct model name here
        fields = ['name', 'email', 'message']
        verbose_name = "Contact Form Submission"
        verbose_name_plural = "Contact Form Submissions"
        ordering = ['-created_at']
