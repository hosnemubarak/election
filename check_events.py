import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'election_site.settings')
django.setup()
from core.models import Event
try:
    for e in Event.objects.all():
        print(f"Event ID: {e.id}")
        print(f"  Title: {ascii(e.title)}")
        print(f"  Location: {ascii(e.location)}")
        print(f"  Date: {e.date}")
except Exception as e:
    print(f"Error: {e}")
