import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_site.settings')
django.setup()

from core.models import Video
from django.core.files.base import ContentFile

# Clear existing videos
Video.objects.all().delete()

# Demo videos data
videos_data = [
    {
        'title': 'ক্যাম্পেইন নির্বাচনী বক্তব্য',
        'youtube_url': 'https://www.youtube.com/watch?v=TkCIgI74970',
    },
    {
        'title': 'হেলথ কেয়ার টাউন হল',
        'youtube_url': 'https://www.youtube.com/watch?v=TkCIgI74970',
    },
    {
        'title': 'সাক্ষাৎকার: শিক্ষার জন্য দৃষ্টিভঙ্গি',
        'youtube_url': 'https://www.youtube.com/watch?v=TkCIgI74970',
    },
]

# Create placeholder thumbnail (1x1 pixel image)
placeholder_image = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'

for idx, video_data in enumerate(videos_data, 1):
    video = Video.objects.create(
        title=video_data['title'],
        youtube_url=video_data['youtube_url'],
    )
    
    # Save placeholder thumbnail
    video.thumbnail.save(f'video_{idx}.png', ContentFile(placeholder_image), save=True)
    
    print(f"Created video with ID: {video.id}")

print(f"\nSuccessfully created {Video.objects.count()} videos!")
