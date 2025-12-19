import os
import django
from django.conf import settings
from django.core.files import File
from datetime import date, timedelta

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_site.settings')
django.setup()

from core.models import Event

def populate_events():
    # Clear existing events
    print("Clearing existing events...")
    Event.objects.all().delete()

    # Ensure media directory exists
    media_events_dir = settings.MEDIA_ROOT / 'events'
    media_events_dir.mkdir(parents=True, exist_ok=True)
    
    events_data = [
        {
            "title": "টাউন হল মিটিং",
            "date": date.today() + timedelta(days=7),
            "location": "ঢাকা কমিউনিটি সেন্টার",
            "description": "খোলামেলা আলোচনায় যুক্ত হন।",
            "image_src": "HomePag1e.png", 
            "image_dest": "town_hall.png"
        },
        {
            "title": "ইউথ সামিট",
            "date": date.today() + timedelta(days=14),
            "location": "ন্যাশনাল ইউনিভার্সিটি",
            "description": "যুব সমাজের নেতৃত্ব বিকাশ।",
            "image_src": "HomePage-2.png",
            "image_dest": "youth_summit.png"
        },
        {
            "title": "হেলথকেয়ার ওয়ার্কশপ",
            "date": date.today() + timedelta(days=21),
            "location": "সেন্ট্রাল হাসপাতাল",
            "description": "স্বাস্থ্যখাতের উন্নয়ন বিষয়ে মতবিনিময়।",
            "image_src": "HomePage-1.png",
            "image_dest": "healthcare_workshop.png"
        }
    ]

    static_images_dir = settings.BASE_DIR / 'static' / 'assets' / 'images'

    for data in events_data:
        src_path = static_images_dir / data['image_src']
        if not src_path.exists():
            print(f"Error: Image {src_path} not found.")
            continue

        # Create Event
        event = Event(
            title=data['title'],
            date=data['date'],
            location=data['location'],
            description=data['description']
        )
        
        # Open the image file and save it to the ImageField
        with open(src_path, 'rb') as f:
            event.image.save(data['image_dest'], File(f), save=True)
        
        print(f"Created event with ID: {event.id}")

if __name__ == '__main__':
    populate_events()
