from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'body']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Summarize your experience (e.g. Blazing fast FPS in 4K)'}),
            'body': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your detailed hardware performance benchmarks, thermal readings, and experience...'}),
        }
