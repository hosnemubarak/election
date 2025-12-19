from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('manifesto/', views.manifesto, name='manifesto'),
    path('media/', views.media, name='media'),
    path('donation/', views.donation, name='donation'),
    path('contact/', views.contact, name='contact'),
]
