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
    
    name = models.CharField(max_length=200, verbose_name='নাম')
    email = models.EmailField(verbose_name='ইমেইল')
    phone = models.CharField(max_length=20, verbose_name='ফোন নম্বর')
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES, verbose_name='বিভাগ')
    message = models.TextField(verbose_name='বার্তা')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='প্রেরণের সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')
    
    class Meta:
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তাসমূহ'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.department} ({self.created_at.strftime('%d %b %Y')})"
