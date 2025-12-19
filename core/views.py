from django.shortcuts import render, get_object_or_404
from .models import Event, PressRelease, Video

def home(request):
    events = Event.objects.all()[:3]
def home(request):
    events = Event.objects.all()[:3]
    return render(request, 'home.html', {'events': events})

def events(request):
    events = Event.objects.all()
    return render(request, 'events.html', {'events': events})

def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request, 'event_detail.html', {'event': event})

def about(request):
    return render(request, 'about.html')

def manifesto(request):
    return render(request, 'manifesto.html')

def media(request):
    press_releases = PressRelease.objects.all()[:3]
    videos = Video.objects.all()[:3]
    return render(request, 'media.html', {'press_releases': press_releases, 'videos': videos})

def press_releases(request):
    press_releases = PressRelease.objects.all()
    return render(request, 'press_releases.html', {'press_releases': press_releases})

def press_release_detail(request, pk):
    press = get_object_or_404(PressRelease, pk=pk)
    return render(request, 'press_release_detail.html', {'press': press})

def videos(request):
    videos = Video.objects.all()
    return render(request, 'videos.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(Video, pk=pk)
    return render(request, 'video_detail.html', {'video': video})

def donation(request):
    return render(request, 'donation.html')

def contact(request):
    return render(request, 'contact.html')
