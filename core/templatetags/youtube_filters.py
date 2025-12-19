from django import template
import re

register = template.Library()

@register.filter
def youtube_id(url):
    """
    Extract YouTube video ID from various URL formats:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    """
    if not url:
        return ''
    
    # Pattern for watch?v= format
    match = re.search(r'(?:v=|/)([0-9A-Za-z_-]{11}).*', url)
    if match:
        return match.group(1)
    
    return ''
