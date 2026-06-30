# AI-Solutions — Django Backend System

### Project Overview
Full-stack Django web application converting the AI-Solutions frontend into a complete backend-integrated system with SQLite database, Django authentication, and dynamic content rendering.

---

### Setup Instructions

**Requirements:** Python 3.10+, pip

```bash
# 1. Install Django
pip install django

# 2. Run migrations
python manage.py migrate

# 3. Create superuser (or use the default: admin / admin123)
python manage.py createsuperuser

# 4. Seed sample data (already done — db.sqlite3 included)
# python manage.py shell < seed.py

# 5. Start the development server
python manage.py runserver

# 6. Open in browser
# http://127.0.0.1:8000/
```

---

### Default Admin Credentials
- **URL:** http://127.0.0.1:8000/admin-login/
- **Username:** admin
- **Password:** admin123

Django Admin panel: http://127.0.0.1:8000/django-admin/

---

### URL Structure

| URL | Page | Description |
|-----|------|-------------|
| / | Home | Landing page |
| /services/ | Services | DB-driven AI services |
| /articles/ | Articles | DB-driven articles |
| /events/ | Events | DB-driven events |
| /contact/ | Contact | Enquiry form → SQLite |
| /feedback/ | Feedback | Feedback form → SQLite |
| /admin-login/ | Admin Login | Django session auth |
| /admin-dashboard/ | Dashboard | Dynamic admin panel |
| /django-admin/ | Django Admin | ORM management panel |

---

### Architecture

```
ai_solutions/          ← Django project root
├── ai_solutions/      ← Project configuration
│   ├── settings.py    ← SQLite, static files, apps
│   └── urls.py        ← Root URL routing
├── core/              ← Main views module
│   └── views.py       ← All view functions
├── enquiries/         ← Enquiry management app
│   ├── models.py      ← Enquiry model
│   └── forms.py       ← EnquiryForm
├── feedback/          ← Feedback management app
│   ├── models.py      ← Feedback model
│   └── forms.py       ← FeedbackForm
├── content/           ← Content management app
│   └── models.py      ← AIService, Article, Event, ChatbotResponse
├── templates/         ← All Django HTML templates
├── static/            ← CSS, JS assets (original, unchanged)
│   ├── css/style.css
│   └── js/script.js
└── db.sqlite3         ← SQLite database (pre-seeded)
```

---

### Database Models

| Model | App | Key Fields |
|-------|-----|------------|
| Enquiry | enquiries | full_name, email, subject, message, status |
| Feedback | feedback | full_name, rating, message, status |
| AIService | content | icon, title, description, is_active |
| Article | content | title, category, excerpt, status |
| Event | content | title, event_type, event_date, location, is_upcoming |
| ChatbotResponse | content | question, answer, is_active |

---

### Module Alignment with Documentation

| Module | Implementation |
|--------|---------------|
| Authentication Module | Django `contrib.auth` session login |
| Enquiry Management | `Enquiry` model + contact form POST |
| Feedback Management | `Feedback` model + feedback form POST |
| Dashboard Dynamic Data | `@login_required` view with ORM queries |
| Articles Module | `Article` model, status-filtered rendering |
| Events Module | `Event` model, upcoming/past filtering |
| AI Services Module | `AIService` model, is_active filtering |
| Chatbot Management | `ChatbotResponse` model + AJAX edit |
| CSRF Protection | `{% csrf_token %}` on all forms |
| Django Session Auth | Replaces JS sessionStorage |
| SQLite Database | `db.sqlite3` via Django ORM |
