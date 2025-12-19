from django import forms
from captcha.fields import CaptchaField
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    captcha = CaptchaField(
        label='যাচাইকরণ কোড',
        help_text='উপরের ছবিতে দেখানো অক্ষরগুলি লিখুন',
        error_messages={
            'invalid': 'যাচাইকরণ কোড সঠিক নয়। অনুগ্রহ করে আবার চেষ্টা করুন।',
            'required': 'যাচাইকরণ কোড প্রয়োজন।'
        }
    )
    
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
