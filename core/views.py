from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, PressRelease, Video
from .forms import ContactForm, CommentForm

def home(request):
    """Home page with latest 3 events, 6 videos, and 3 press releases"""
    events = Event.objects.all()[:3]
    videos = Video.objects.all()[:6]
    press_releases = PressRelease.objects.all()[:3]
    return render(request, 'home.html', {
        'events': events,
        'videos': videos,
        'press_releases': press_releases
    })

def events(request):
    """Events listing page"""
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_detail(request, slug):
    """Individual event detail page"""
    event = get_object_or_404(Event, slug=slug)
    return render(request, 'event_detail.html', {'event': event})

def about(request):
    """About page"""
    return render(request, 'about.html')

def manifesto(request):
    """Manifesto page"""
    return render(request, 'manifesto.html')

def news_media(request):
    """News media page with latest press releases and videos"""
    press_releases = PressRelease.objects.all()[:3]
    videos = Video.objects.all()[:3]
    return render(request, 'news_media.html', {'press_releases': press_releases, 'videos': videos})

def press_releases(request):
    """Press releases listing page"""
    press_releases = PressRelease.objects.all()
    return render(request, 'press_releases.html', {'press_releases': press_releases})

def press_release_detail(request, slug):
    """Individual press release detail page"""
    press = get_object_or_404(PressRelease, slug=slug)
    return render(request, 'press_release_detail.html', {'press': press})

def videos(request):
    """Videos listing page"""
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})

def video_detail(request, slug):
    """Individual video detail page"""
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


def comments(request):
    """Comments/Feedback page for user opinions"""
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'আপনার মতামত সফলভাবে জমা হয়েছে। আপনার মূল্যবান মতামতের জন্য ধন্যবাদ।')
            return redirect('comments')
        else:
            messages.error(request, 'ফর্মটি পূরণ করতে সমস্যা হয়েছে। অনুগ্রহ করে সকল ক্ষেত্র সঠিকভাবে পূরণ করুন।')
    else:
        form = CommentForm()
    
    return render(request, 'comments.html', {'form': form})

# Custom error handlers
def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

def custom_403(request, exception):
    return render(request, '403.html', status=403)

def custom_400(request, exception):
    return render(request, '400.html', status=400)

def robots_txt(request):
    """Serve robots.txt file"""
    from django.http import HttpResponse
    lines = [
        "# robots.txt for najmulmostafaamin.com",
        "# This file tells search engines which pages to crawl",
        "",
        "# Allow all search engines to crawl all pages",
        "User-agent: *",
        "Allow: /",
        "",
        "# Disallow admin panel (security best practice)",
        "Disallow: /admin/",
        "",
        "# Sitemap location",
        "# Search engines will automatically discover and crawl all pages listed here",
        "Sitemap: https://najmulmostafaamin.com/sitemap.xml",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

