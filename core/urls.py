from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'),
    path('press/', views.press_releases, name='press_releases'),
    path('press/<int:pk>/', views.press_release_detail, name='press_release_detail'),
    path('videos/', views.videos, name='videos'),
    path('videos/<int:pk>/', views.video_detail, name='video_detail'),
    path('about/', views.about, name='about'),
    path('manifesto/', views.manifesto, name='manifesto'),
    path('media/', views.media, name='media'),
    path('contact/', views.contact, name='contact'),
    path('captcha/', include('captcha.urls')),
]
