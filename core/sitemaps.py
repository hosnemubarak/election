"""
Django Sitemap Configuration for SEO Optimization
==================================================

This module defines sitemap classes for both static and dynamic content.
Sitemaps help search engines discover and index website pages efficiently.

SEO Best Practices Implemented:
- Priority: Indicates relative importance of pages (0.0 to 1.0)
- Changefreq: Hints how often content changes
- Lastmod: Last modification date for better crawl efficiency
- Pagination: Handles large datasets (50,000 URLs per sitemap file)
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Event, PressRelease, Video


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static pages (home, about, contact, etc.)
    
    Priority Guidelines:
    - 1.0: Homepage (most important)
    - 0.8: Key pages (about, manifesto)
    - 0.6: Secondary pages (contact, media)
    
    Changefreq Guidelines:
    - 'always': Homepage (frequently updated)
    - 'weekly': About, manifesto (occasionally updated)
    - 'monthly': Contact (rarely updated)
    """
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        """
        Return list of static page URL names.
        Each item will be passed to location() method.
        """
        return [
            'home',           # Homepage - highest priority
            'about',          # About page
            'manifesto',      # Manifesto page
            'news_media',     # News/Media page
            'events',         # Events listing
            'press_releases', # Press releases listing
            'videos',         # Videos listing
            'contact',        # Contact page
        ]
    
    def location(self, item):
        """
        Convert URL name to actual URL path.
        Django reverse() generates the full URL path.
        """
        return reverse(item)
    
    def priority(self, item):
        """
        Dynamic priority based on page importance.
        Homepage gets highest priority (1.0).
        """
        priorities = {
            'home': 1.0,           # Homepage - most important
            'about': 0.9,          # About - very important
            'manifesto': 0.9,      # Manifesto - very important
            'news_media': 0.7,     # Media hub - important
            'events': 0.7,         # Events listing - important
            'press_releases': 0.7, # Press listing - important
            'videos': 0.7,         # Videos listing - important
            'contact': 0.6,        # Contact - moderately important
        }
        return priorities.get(item, 0.5)
    
    def changefreq(self, item):
        """
        Dynamic change frequency based on content type.
        More dynamic pages get higher frequency.
        """
        frequencies = {
            'home': 'daily',           # Homepage changes frequently
            'about': 'monthly',        # Static content
            'manifesto': 'monthly',    # Static content
            'news_media': 'daily',     # Aggregated content
            'events': 'weekly',        # New events added regularly
            'press_releases': 'weekly',# New press releases
            'videos': 'weekly',        # New videos
            'contact': 'yearly',       # Rarely changes
        }
        return frequencies.get(item, 'monthly')


class EventSitemap(Sitemap):
    """
    Sitemap for Event model instances.
    
    SEO Considerations:
    - Shows all events (past and future)
    - Ordered by date (newest first)
    - Includes last modification date
    - Medium priority (0.6) - detail pages
    """
    changefreq = 'weekly'
    priority = 0.6
    
    def items(self):
        """
        Return all Event objects.
        Ordered by date (newest first) for better crawl priority.
        """
        return Event.objects.all().order_by('-date')
    
    def lastmod(self, obj):
        """
        Return last modification date.
        Uses event date as proxy for modification.
        This helps search engines prioritize recent content.
        """
        return obj.date
    
    def location(self, obj):
        """
        Generate URL for event detail page.
        Uses the event's slug for SEO-friendly URLs.
        """
        return reverse('event_detail', args=[obj.slug])


class PressReleaseSitemap(Sitemap):
    """
    Sitemap for PressRelease model instances.
    
    SEO Considerations:
    - All published press releases
    - Higher priority (0.7) - news content is important
    - Weekly change frequency
    - Includes publication date
    """
    changefreq = 'weekly'
    priority = 0.7
    
    def items(self):
        """
        Return all PressRelease objects.
        Ordered by date (newest first).
        """
        return PressRelease.objects.all().order_by('-date')
    
    def lastmod(self, obj):
        """
        Return publication date as last modification.
        Helps search engines prioritize recent news.
        """
        return obj.date
    
    def location(self, obj):
        """
        Generate URL for press release detail page.
        Uses the press release's slug.
        """
        return reverse('press_release_detail', args=[obj.slug])


class VideoSitemap(Sitemap):
    """
    Sitemap for Video model instances.
    
    SEO Considerations:
    - All videos
    - Medium priority (0.6)
    - Weekly change frequency
    - Includes creation timestamp
    """
    changefreq = 'weekly'
    priority = 0.6
    
    def items(self):
        """
        Return all Video objects.
        Ordered by creation date (newest first).
        """
        return Video.objects.all().order_by('-created_at')
    
    def lastmod(self, obj):
        """
        Return creation date as last modification.
        Videos typically don't change after creation.
        """
        return obj.created_at
    
    def location(self, obj):
        """
        Generate URL for video detail page.
        Uses the video's slug.
        """
        return reverse('video_detail', args=[obj.slug])


# ==============================================================================
# ADVANCED: Pagination for Large Datasets
# ==============================================================================
# If you have more than 50,000 URLs in a single sitemap, use pagination:
#
# class LargePressReleaseSitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0.7
#     limit = 50000  # Maximum URLs per sitemap file
#     
#     def items(self):
#         return PressRelease.objects.all().order_by('-date')
#     
#     def lastmod(self, obj):
#         return obj.date
#
# Django will automatically create:
# - /sitemap.xml (index file)
# - /sitemap-pressrelease-1.xml
# - /sitemap-pressrelease-2.xml
# - etc.
# ==============================================================================
