"""
URL configuration for election_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, EventSitemap, PressReleaseSitemap, VideoSitemap

# Sitemap configuration
# Dictionary maps sitemap names to sitemap classes
sitemaps = {
    'static': StaticViewSitemap,        # Static pages (home, about, etc.)
    'events': EventSitemap,             # Event detail pages
    'press': PressReleaseSitemap,       # Press release detail pages
    'videos': VideoSitemap,             # Video detail pages
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    # Sitemap URL - accessible at /sitemap.xml
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
handler400 = 'core.views.custom_400'

from django.conf import settings
from django.conf.urls.static import static
from core.views import robots_txt

# Serve robots.txt
urlpatterns += [
    path('robots.txt', robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    from django.views.static import serve
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
