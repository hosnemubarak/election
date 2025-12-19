from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event, PressRelease, Video
from .forms import ContactForm

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

