from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()
    location = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='events/')

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

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    youtube_url = models.URLField()
    thumbnail = models.ImageField(upload_to='videos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def get_video_id(self):
        """Extract YouTube video ID from URL"""
        import re
        if not self.youtube_url:
            return ''
        match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', self.youtube_url)
        return match.group(1) if match else ''

