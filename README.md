# Election Website

A Django-based election information website featuring static pages, media galleries, contact forms with CAPTCHA verification, and a clean, professional design.

## 🌟 Features

- **Static Pages**: Home, About, Media, Contact, and additional informational pages
- **Contact Form**: Secure contact form with django-simple-captcha for spam prevention
- **Media Gallery**: Display election-related media and content
- **Responsive Design**: Bootstrap 5 integration for mobile-friendly layouts
- **Admin Panel**: Django admin interface for managing content and contact submissions
- **Environment-Based Configuration**: Secure configuration management using environment variables

## 🛠️ Technology Stack

- **Framework**: Django 6.0
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Security**: django-simple-captcha for form verification
- **Server**: Gunicorn (production)
- **Environment Management**: django-environ

## 📋 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd election
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Copy the example file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

Edit `.env` and configure the following variables:

```env
# Django Settings
SECRET_KEY=your-unique-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Timezone
TIME_ZONE=UTC
```

> **⚠️ Important**: Generate a new SECRET_KEY for production! You can use:
> ```python
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
election/
├── core/                      # Main application
│   ├── migrations/           # Database migrations
│   ├── models.py            # Data models (ContactMessage, etc.)
│   ├── views.py             # View functions
│   ├── forms.py             # Form definitions
│   └── admin.py             # Admin panel configuration
├── election_site/            # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── templates/                # HTML templates
│   ├── base.html            # Base template
│   ├── navbar.html          # Navigation bar
│   ├── footer.html          # Footer
│   └── pages/               # Page templates
├── static/                   # Static files (CSS, JS, images)
├── media/                    # User-uploaded files
├── .env                      # Environment variables (not in git)
├── .env.example             # Environment template
├── requirements.txt         # Python dependencies
└── manage.py                # Django management script
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Django secret key for cryptographic signing | - | ✅ Yes |
| `DEBUG` | Enable/disable debug mode | `False` | ✅ Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | `[]` | ✅ Yes |
| `TIME_ZONE` | Application timezone | `UTC` | ❌ No |

### Database Configuration

The project uses SQLite by default for development. For production, configure PostgreSQL:

1. Install PostgreSQL and create a database
2. Update `.env` with database credentials:
   ```env
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432
   ```
3. Update `settings.py` to use these variables

## 📝 Usage

### Accessing the Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Log in with your superuser credentials
3. Manage contact messages, users, and other content

### Available Pages

- **Home**: `/` - Main landing page
- **About**: `/about/` - About the election
- **Media**: `/media/` - Media gallery
- **Contact**: `/contact/` - Contact form with CAPTCHA

### Managing Contact Submissions

Contact form submissions are stored in the database and can be viewed/managed through the Django admin panel under "Contact Messages".

## 🧪 Development

### Running Tests

```bash
python manage.py test
```

### Collecting Static Files (Production)

```bash
python manage.py collectstatic
```

### Creating New Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate a new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up Gunicorn or uWSGI
- [ ] Configure reverse proxy (Nginx/Apache)
- [ ] Enable HTTPS/SSL
- [ ] Set up proper logging
- [ ] Configure backup strategy

### Running with Gunicorn

```bash
gunicorn election_site.wsgi:application --bind 0.0.0.0:8000
```

## 🔒 Security Notes

- Never commit `.env` file to version control
- Always use strong, unique `SECRET_KEY` in production
- Keep `DEBUG=False` in production
- Regularly update dependencies for security patches
- Use HTTPS in production
- Configure proper CORS and CSRF settings

## 📦 Dependencies

See `requirements.txt` for a complete list. Key dependencies:

- `Django==6.0` - Web framework
- `django-environ==0.12.0` - Environment variable management
- `django-simple-captcha==0.6.3` - CAPTCHA for forms
- `gunicorn==23.0.0` - WSGI HTTP server
- `pillow==12.0.0` - Image processing
- `psycopg2-binary==2.9.11` - PostgreSQL adapter

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Support

For issues, questions, or contributions, please open an issue on the project repository.

---

**Made with ❤️ using Django**
