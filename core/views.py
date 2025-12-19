from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def manifesto(request):
    return render(request, 'manifesto.html')

def media(request):
    return render(request, 'media.html')

def donation(request):
    return render(request, 'donation.html')

def contact(request):
    return render(request, 'contact.html')
