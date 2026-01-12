from django import forms
from .models import ContactMessage, Comment

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'upazila', 'union', 'department', 'message']
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
            'upazila': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_upazila'
            }),
            'union': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_union'
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
            'upazila': 'উপজেলা',
            'union': 'ইউনিয়ন/পৌরসভা',
            'department': 'বিভাগ',
            'message': 'বার্তা',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        upazila = cleaned_data.get('upazila')
        union = cleaned_data.get('union')
        
        if upazila and union:
            valid_unions = ContactMessage.UPAZILA_UNION_MAP.get(upazila, [])
            if union not in valid_unions:
                raise forms.ValidationError({
                    'union': 'নির্বাচিত ইউনিয়ন/পৌরসভা এই উপজেলার জন্য বৈধ নয়। অনুগ্রহ করে সঠিক ইউনিয়ন/পৌরসভা নির্বাচন করুন।'
                })
        
        return cleaned_data


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'upazila', 'union', 'subject', 'category', 'rating', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'আপনার পূর্ণ নাম লিখুন'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ইমেইল ঠিকানা'
            }),
            'upazila': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_comment_upazila'
            }),
            'union': forms.Select(attrs={
                'class': 'form-select',
                'id': 'id_comment_union'
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
            'upazila': 'উপজেলা',
            'union': 'ইউনিয়ন/পৌরসভা',
            'subject': 'বিষয়',
            'category': 'মতামতের ধরন',
            'rating': 'মূল্যায়ন (ঐচ্ছিক)',
            'message': 'আপনার মতামত',
        }
    
    def clean(self):
        cleaned_data = super().clean()
        upazila = cleaned_data.get('upazila')
        union = cleaned_data.get('union')
        
        if upazila and union:
            valid_unions = Comment.UPAZILA_UNION_MAP.get(upazila, [])
            if union not in valid_unions:
                raise forms.ValidationError({
                    'union': 'নির্বাচিত ইউনিয়ন/পৌরসভা এই উপজেলার জন্য বৈধ নয়। অনুগ্রহ করে সঠিক ইউনিয়ন/পৌরসভা নির্বাচন করুন।'
                })
        
        return cleaned_data
