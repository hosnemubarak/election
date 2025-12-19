from django.contrib import admin
from .models import Event, PressRelease, Video, ContactMessage

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)

@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'category')
    list_filter = ('date', 'category')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'created_at', 'is_read')
    list_filter = ('department', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

