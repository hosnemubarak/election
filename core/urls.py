from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.events, name='events'),
    path('events/<str:slug>/', views.event_detail, name='event_detail'),
    path('press/', views.press_releases, name='press_releases'),
    path('press/<str:slug>/', views.press_release_detail, name='press_release_detail'),
    path('videos/', views.videos, name='videos'),
    path('videos/<str:slug>/', views.video_detail, name='video_detail'),
    path('about/', views.about, name='about'),
    path('manifesto/', views.manifesto, name='manifesto'),
    path('press-release/', views.media, name='media'),
    path('contact/', views.contact, name='contact'),
    path('captcha/', include('captcha.urls')),
]

