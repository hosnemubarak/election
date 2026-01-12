from django import forms
from .models import ContactMessage, Comment

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'department', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'আপনার পূর্ণ নাম লিখুন'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ইমেইল ঠিকানা'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+880 123 45677'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'আপনার বার্তা লিখুন...'
            }),
        }
        labels = {
            'name': 'আপনার নাম',
            'email': 'ইমেইল',
            'phone': 'ফোন নম্বর',
            'department': 'বিভাগ',
            'message': 'বার্তা',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'subject', 'category', 'rating', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'আপনার পূর্ণ নাম লিখুন'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ইমেইল ঠিকানা'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'বিষয় (ঐচ্ছিক)'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'আপনার মতামত বিস্তারিত লিখুন...'
            }),
        }
        labels = {
            'name': 'আপনার নাম',
            'email': 'ইমেইল',
            'subject': 'বিষয়',
            'category': 'মতামতের ধরন',
            'rating': 'মূল্যায়ন (ঐচ্ছিক)',
            'message': 'আপনার মতামত',
        }
