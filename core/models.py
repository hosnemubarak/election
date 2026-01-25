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
        ('satkania', 'সাতকানিয়া'),
        ('lohagara', 'লোহাগাড়া'),
    ]
    
    UNION_CHOICES = [
        # -------- Lohagara --------
        ('lohagara_union', 'লোহাগাড়া ইউনিয়ন'),
        ('padua', 'পদুয়া'),
        ('barahatia', 'বড়হাতিয়া'),
        ('amirabad', 'আমিরাবাদ'),
        ('adhunagar', 'আধুনগর'),
        ('chunati', 'চুনতি'),
        ('charamba', 'চরম্বা'),
        ('putibila', 'পুটিবিলা'),
        ('kalauzan', 'কলাউজান'),

        # -------- Satkania (All Unions) --------
        ('charti', '১নং চরতী'),
        ('khagria', '২নং খাগরিয়া'),
        ('nalua', '৩নং নলুয়া'),
        # ('kanchana', '৪নং কাঞ্চনা'),
        ('amilais', '৫নং আমিলাইষ'),
        ('eochia', '৬নং এওচিয়া'),
        ('madarsha', '৭নং মাদার্শা'),
        ('dhemsha', '৮নং ঢেমশা'),
        ('paschim_dhemsha', '৯নং পশ্চিম ঢেমশা'),
        # ('keochia', '১০নং কেঁওচিয়া'),
        # ('kaliaish', '১১নং কালিয়াইশ'),
        # ('dharmapur', '১২নং ধর্মপুর'),
        # ('bazalia', '১৩নং বাজালিয়া'),
        # ('purangar', '১৪নং পুরানগড়'),
        ('chadaha', '১৫নং ছদাহা'),
        ('satkania_union', '১৬নং সাতকানিয়া'),
        ('sonakania', '১৭নং সোনাকানিয়া'),
        # -------- Satkania Pourashava --------
        ('satkania_pourashava', 'সাতকানিয়া পৌরসভা'),
        ]

    UPAZILA_UNION_MAP = {
        'lohagara': [
            'lohagara_union',
            'padua',
            'barahatia',
            'amirabad',
            'adhunagar',
            'chunati',
            'charamba',
            'putibila',
            'kalauzan',
        ],
        'satkania': [
                'charti',
                'khagria',
                'nalua',
                # 'kanchana',
                'amilais',
                'eochia',
                'madarsha',
                'dhemsha',
                'paschim_dhemsha',
                # 'keochia',
                # 'kaliaish',
                # 'dharmapur',
                # 'bazalia',
                # 'purangar',
                'chadaha',
                'satkania_union',
                'sonakania',
                'satkania_pourashava',
            ]
        }
    
    
    name = models.CharField(max_length=200, verbose_name='নাম', blank=True)
    email = models.EmailField(verbose_name='ইমেইল', blank=True)
    phone = models.CharField(max_length=20, verbose_name='ফোন নম্বর', blank=True)
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
    
    UPAZILA_CHOICES = [
        ('satkania', 'সাতকানিয়া'),
        ('lohagara', 'লোহাগাড়া'),
    ]
    
    UNION_CHOICES = [
        # -------- Lohagara --------
        ('lohagara_union', 'লোহাগাড়া ইউনিয়ন'),
        ('padua', 'পদুয়া'),
        ('barahatia', 'বড়হাতিয়া'),
        ('amirabad', 'আমিরাবাদ'),
        ('adhunagar', 'আধুনগর'),
        ('chunati', 'চুনতি'),
        ('charamba', 'চরম্বা'),
        ('putibila', 'পুটিবিলা'),
        ('kalauzan', 'কলাউজান'),

        # -------- Satkania (All Unions) --------
        ('charti', '১নং চরতী'),
        ('khagria', '২নং খাগরিয়া'),
        ('nalua', '৩নং নলুয়া'),
        # ('kanchana', '৪নং কাঞ্চনা'),
        ('amilais', '৫নং আমিলাইষ'),
        ('eochia', '৬নং এওচিয়া'),
        ('madarsha', '৭নং মাদার্শা'),
        ('dhemsha', '৮নং ঢেমশা'),
        ('paschim_dhemsha', '৯নং পশ্চিম ঢেমশা'),
        # ('keochia', '১০নং কেঁওচিয়া'),
        # ('kaliaish', '১১নং কালিয়াইশ'),
        # ('dharmapur', '১২নং ধর্মপুর'),
        # ('bazalia', '১৩নং বাজালিয়া'),
        # ('purangar', '১৪নং পুরানগড়'),
        ('chadaha', '১৫নং ছদাহা'),
        ('satkania_union', '১৬নং সাতকানিয়া'),
        ('sonakania', '১৭নং সোনাকানিয়া'),
        # -------- Satkania Pourashava --------
        ('satkania_pourashava', 'সাতকানিয়া পৌরসভা'),
        ]

    UPAZILA_UNION_MAP = {
        'lohagara': [
            'lohagara_union',
            'padua',
            'barahatia',
            'amirabad',
            'adhunagar',
            'chunati',
            'charamba',
            'putibila',
            'kalauzan',
        ],
        'satkania': [
                'charti',
                'khagria',
                'nalua',
                # 'kanchana',
                'amilais',
                'eochia',
                'madarsha',
                'dhemsha',
                'paschim_dhemsha',
                # 'keochia',
                # 'kaliaish',
                # 'dharmapur',
                # 'bazalia',
                # 'purangar',
                'chadaha',
                'satkania_union',
                'sonakania',
                'satkania_pourashava',
            ]
        }
    
    WARD_CHOICES = [
        ('1', '১'),
        ('2', '২'),
        ('3', '৩'),
        ('4', '৪'),
        ('5', '৫'),
        ('6', '৬'),
        ('7', '৭'),
        ('8', '৮'),
        ('9', '৯'),
    ]
    
    
    name = models.CharField(max_length=200, verbose_name='নাম')
    mobile = models.CharField(max_length=20, verbose_name='মোবাইল নম্বর', blank=True, default='')
    upazila = models.CharField(max_length=50, choices=UPAZILA_CHOICES, verbose_name='উপজেলা', default='satkania')
    union = models.CharField(max_length=50, choices=UNION_CHOICES, verbose_name='ইউনিয়ন/পৌরসভা', default='satkania_union')
    ward = models.CharField(max_length=10, choices=WARD_CHOICES, verbose_name='ওয়ার্ড', default='1')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='ধরন')
    message = models.TextField(verbose_name='মতামত')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='প্রেরণের সময়')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')
    is_published = models.BooleanField(default=False, verbose_name='প্রকাশিত')
    
    class Meta:
        verbose_name = 'মতামত'
        verbose_name_plural = 'মতামতসমূহ'
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
