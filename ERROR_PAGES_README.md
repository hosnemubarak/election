# Custom Error Pages Configuration

This document explains how to test and configure custom error pages in Django.

## Testing Error Pages in Development

Since `DEBUG = True` in development, Django shows detailed error pages instead of custom error templates. To test custom error pages:

### Method 1: Temporarily Set DEBUG = False

1. In `settings.py`, change:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']
   ```

2. Restart server and visit:
   - `/test-404/` for 404 page
   - `/test-500/` for 500 page
   - `/test-403/` for 403 page
   - `/test-400/` for 400 page

3. **Remember to set `DEBUG = True` again after testing!**

### Method 2: Create Test URLs (Recommended)

Add these temporary URLs to `core/urls.py`:

```python
# Test error pages (remove in production)
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request

urlpatterns = [
    # ... existing patterns ...
    path('test-404/', lambda r: page_not_found(r, None)),
    path('test-500/', lambda r: server_error(r)),
    path('test-403/', lambda r: permission_denied(r, None)),
    path('test-400/', lambda r: bad_request(r, None)),
]
```

## Production Configuration

For production deployment, ensure:

1. `DEBUG = False` in settings.py
2. `ALLOWED_HOSTS` includes your domain
3. Error handlers are configured in main urls.py:
   ```python
   handler404 = 'core.views.custom_404'
   handler500 = 'core.views.custom_500'
   handler403 = 'core.views.custom_403'
   handler400 = 'core.views.custom_400'
   ```

## Error Pages Created

- **404.html** - Page Not Found
- **500.html** - Server Error
- **403.html** - Permission Denied
- **400.html** - Bad Request

All pages extend `base.html` and maintain consistent design with the rest of the site.
