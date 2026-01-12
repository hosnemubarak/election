from django.db import models
from django.utils.text import slugify
import re

def custom_slugify(value):
    # Keep Bangla characters, alphanumeric, and hyphens
    value = re.sub(r'[^\u0980-\u09ff\w\s-]', '', value)
    return re.sub(r'[-\s]+', '-', value).strip('-')

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def get_image_url(self):
        """Return image URL or default image if no image uploaded"""
        if self.image:
            return self.image.url
        return '/static/assets/images/thumbnil.png'

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class PressRelease(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    category = models.CharField(max_length=100, help_text="e.g., Policy, Campaign")
    summary = models.TextField()
    content = models.TextField()
    document = models.FileField(upload_to='press_releases/docs/', blank=True, null=True)
    image = models.ImageField(upload_to='press_releases/images/', blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    thumbnail = models.ImageField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = custom_slugify(self.title)
        super().save(*args, **kwargs)

    def get_thumbnail_url(self):
        """Return thumbnail URL, YouTube thumbnail, or default image"""
        if self.thumbnail:
            return self.thumbnail.url
        
        # Try to get YouTube thumbnail
        video_id = self.get_video_id()
        if video_id:
            # YouTube provides thumbnails at different qualities
            # maxresdefault.jpg (1920x1080) - highest quality
            # sddefault.jpg (640x480) - standard quality
            # hqdefault.jpg (480x360) - high quality
            # mqdefault.jpg (320x180) - medium quality
            # default.jpg (120x90) - default quality
            return f'https://img.youtube.com/vi/{video_id}/maxresdefault.jpg'
        
        # Fallback to static default image
        return '/static/assets/images/thumbnil.png'

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """Extract YouTube video ID from URL"""
        import re
        if not self.youtube_url:
            return ''
        match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', self.youtube_url)
        return match.group(1) if match else ''

class ContactMessage(models.Model):
    DEPARTMENT_CHOICES = [
        ('general', 'সাধারণ জিজ্ঞাসা'),
        ('media', 'মিডিয়া ও প্রেস'),
        ('volunteer', 'স্বেচ্ছাসেবক'),
        ('other', 'অন্যান্য'),
    ]
    
    UPAZILA_CHOICES = [
        ('lohagara', 'লোহাগাড়া'),
        ('satkania', 'সাতকানিয়া'),
    ]
    
    UNION_CHOICES = [
        ('lohagara_union', 'লোহাগাড়া ইউনিয়ন'),
        ('padua', 'পদুয়া'),
        ('barahatia', 'বড়হাতিয়া'),
        ('amirabad', 'আমিরাবাদ'),
        ('adhunagar', 'আধুনগর'),
        ('chunati', 'চুনতি'),
        ('charamba', 'চরাম্বা'),
        ('putibila', 'পুটিবিলা'),
        ('kalauzan', 'কালাউজান'),
        ('satkania_pourashava', 'সাতকানিয়া পৌরসভা'),
        ('satkania_union', 'সাতকানিয়া ইউনিয়ন'),
        ('dhemsha', 'ঢেমশা'),
        ('bazalia', 'বাজালিয়া'),
        ('kanchana', 'কাঞ্চনা'),
        ('keochia', 'কেঁওচিয়া'),
        ('madarsha', 'মাদার্শা'),
        ('purba_guchchagram', 'পূর্ব গুচ্ছগ্রাম'),
    ]
    
    UPAZILA_UNION_MAP = {
        'lohagara': [
            'lohagara_union', 'padua', 'barahatia', 'amirabad', 
            'adhunagar', 'chunati', 'charamba', 'putibila', 'kalauzan'
        ],
        'satkania': [
            'satkania_pourashava', 'satkania_union', 'dhemsha', 'bazalia',
            'kanchana', 'keochia', 'madarsha', 'purba_guchchagram'
        ]
    }
    
    name = models.CharField(max_length=200, verbose_name='নাম')
    email = models.EmailField(verbose_name='ইমেইল')
    phone = models.CharField(max_length=20, verbose_name='ফোন নম্বর')
    upazila = models.CharField(max_length=50, choices=UPAZILA_CHOICES, verbose_name='উপজেলা')
    union = models.CharField(max_length=50, choices=UNION_CHOICES, verbose_name='ইউনিয়ন/পৌরসভা')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, verbose_name='বিভাগ')
    message = models.TextField(verbose_name='বার্তা')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='প্রেরণের সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')
    
    class Meta:
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তাসমূহ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.upazila} - {self.union} ({self.created_at.strftime('%d %b %Y')})"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.upazila and self.union:
            valid_unions = self.UPAZILA_UNION_MAP.get(self.upazila, [])
            if self.union not in valid_unions:
                raise ValidationError({
                    'union': f'নির্বাচিত ইউনিয়ন/পৌরসভা এই উপজেলার জন্য বৈধ নয়।'
                })


class Comment(models.Model):
    CATEGORY_CHOICES = [
        ('general', 'সাধারণ মতামত'),
        ('policy', 'নীতি ও ইশতেহার'),
        ('campaign', 'প্রচারণা'),
        ('suggestion', 'পরামর্শ'),
        ('complaint', 'অভিযোগ'),
        ('appreciation', 'প্রশংসা'),
    ]
    
    RATING_CHOICES = [
        (5, 'অসাধারণ'),
        (4, 'ভালো'),
        (3, 'মাঝারি'),
        (2, 'উন্নতি প্রয়োজন'),
        (1, 'খারাপ'),
    ]
    
    name = models.CharField(max_length=200, verbose_name='নাম')
    email = models.EmailField(verbose_name='ইমেইল')
    subject = models.CharField(max_length=200, verbose_name='বিষয়', blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='ধরন')
    rating = models.IntegerField(choices=RATING_CHOICES, verbose_name='মূল্যায়ন', null=True, blank=True)
    message = models.TextField(verbose_name='মতামত')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='প্রেরণের সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')
    is_published = models.BooleanField(default=False, verbose_name='প্রকাশিত')
    
    class Meta:
        verbose_name = 'মতামত'
        verbose_name_plural = 'মতামতসমূহ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.category} ({self.created_at.strftime('%d %b %Y')})"
