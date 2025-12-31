from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from .models import Event, PressRelease, Video
from .forms import ContactForm

# Cache timeout constants (in seconds)
CACHE_TIMEOUT_SHORT = 300      # 5 minutes - for frequently updated content
CACHE_TIMEOUT_MEDIUM = 900     # 15 minutes - for moderately updated content
CACHE_TIMEOUT_LONG = 3600      # 1 hour - for rarely updated content

@cache_page(CACHE_TIMEOUT_SHORT)
def home(request):
    """Home page with latest 3 events - cached for 5 minutes"""
    events = Event.objects.all()[:3]
    return render(request, 'home.html', {'events': events})

@cache_page(CACHE_TIMEOUT_MEDIUM)
def events(request):
    """Events listing page - cached for 15 minutes"""
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

@cache_page(CACHE_TIMEOUT_LONG)
@vary_on_headers('User-Agent')
def event_detail(request, slug):
    """Individual event detail page - cached for 1 hour"""
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event_detail.html', {'event': event})

@cache_page(CACHE_TIMEOUT_LONG)
def about(request):
    """About page - static content, cached for 1 hour"""
    return render(request, 'about.html')

@cache_page(CACHE_TIMEOUT_LONG)
def manifesto(request):
    """Manifesto page - static content, cached for 1 hour"""
    return render(request, 'manifesto.html')

@cache_page(CACHE_TIMEOUT_SHORT)
def news_media(request):
    """News media page with latest press releases and videos - cached for 5 minutes"""
    press_releases = PressRelease.objects.all()[:3]
    videos = Video.objects.all()[:3]
    return render(request, 'news_media.html', {'press_releases': press_releases, 'videos': videos})

@cache_page(CACHE_TIMEOUT_MEDIUM)
def press_releases(request):
    """Press releases listing page - cached for 15 minutes"""
    press_releases = PressRelease.objects.all()
    return render(request, 'press_releases.html', {'press_releases': press_releases})

@cache_page(CACHE_TIMEOUT_LONG)
@vary_on_headers('User-Agent')
def press_release_detail(request, slug):
    """Individual press release detail page - cached for 1 hour"""
    press = get_object_or_404(PressRelease, slug=slug)
    return render(request, 'press_release_detail.html', {'press': press})

@cache_page(CACHE_TIMEOUT_MEDIUM)
def videos(request):
    """Videos listing page - cached for 15 minutes"""
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})

@cache_page(CACHE_TIMEOUT_LONG)
@vary_on_headers('User-Agent')
def video_detail(request, slug):
    """Individual video detail page - cached for 1 hour"""
    video = get_object_or_404(Video, slug=slug)
    return render(request, 'video_detail.html', {'video': video})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'আপনার বার্তা সফলভাবে প্রেরণ করা হয়েছে। আমরা শীঘ্রই আপনার সাথে যোগাযোগ করব।')
            return redirect('contact')
        else:
            messages.error(request, 'ফর্মটি পূরণ করতে সমস্যা হয়েছে। অনুগ্রহ করে সকল ক্ষেত্র সঠিকভাবে পূরণ করুন।')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

# Custom error handlers
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

