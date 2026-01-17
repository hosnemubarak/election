from django.contrib import admin
from .models import Event, PressRelease, Video, ContactMessage, Comment

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'location')
    search_fields = ('title', 'location')
    list_filter = ('date',)
    exclude = ('slug',)

@admin.register(PressRelease)
class PressReleaseAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'category')
    search_fields = ('title', 'category')
    list_filter = ('date', 'category')
    exclude = ('slug',)

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)
    exclude = ('slug',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'upazila', 'union', 'department', 'created_at', 'is_read')
    list_filter = ('upazila', 'union', 'department', 'is_read', 'created_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'category', 'rating', 'created_at', 'is_read', 'is_published')
    list_filter = ('category', 'rating', 'is_read', 'is_published', 'created_at')
    search_fields = ('name', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_editable = ('is_read', 'is_published')
    date_hierarchy = 'created_at'

