# AI-Solutions 🤖

**AI Services & Enquiry Management System**

A modern Django web application for managing AI services, enquiries, feedback, and events.

🌐 **Live Website**: https://ai-solutions1.onrender.com

---

## 📋 Quick Start

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/SabanamPoudel/Ai-Solutions1.git
cd Ai-Solutions1

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create admin user (optional)
python manage.py createsuperuser

# 6. Start development server
python manage.py runserver
```

Then visit: http://127.0.0.1:8000

---

## 🚀 Deployed Website

The website is **live and publicly accessible** at:

```
https://ai-solutions1.onrender.com
```

### Pages

- **Homepage**: https://ai-solutions1.onrender.com
- **Services**: https://ai-solutions1.onrender.com/services
- **Articles**: https://ai-solutions1.onrender.com/articles
- **Events**: https://ai-solutions1.onrender.com/events
- **Contact**: https://ai-solutions1.onrender.com/contact
- **Admin Login**: https://ai-solutions1.onrender.com/admin-login

---

## 📁 Project Structure

```
ai_solutions/
├── ai_solutions/          # Project configuration
├── content/               # Articles & Events app
├── enquiries/             # Enquiries app
├── feedback/              # Feedback app
├── core/                  # Core features app
├── templates/             # HTML templates
├── static/                # CSS, JavaScript, images
├── media/                 # User uploads
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── DEPLOYMENT.md          # ⭐ Deployment documentation
└── README.md              # This file
```

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|-----------|
| **Framework** | Django 6.0.6 |
| **Server** | Gunicorn |
| **Static Files** | WhiteNoise |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Hosting** | Render.com |
| **Python** | 3.12.0 |

---

## 📦 Dependencies

See `requirements.txt`:

- Django 6.0.6
- asgiref 3.11.1
- sqlparse 0.5.5
- gunicorn 22.0.0
- whitenoise 6.5.0

---

## 🚀 Deployment

The application is deployed on **Render.com** (Free Tier).

**How to deploy:**

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete step-by-step instructions!

### Quick Deployment Summary

1. Push code to GitHub
2. Connect GitHub repo to Render
3. Configure environment variables
4. Render auto-deploys on each push

---

## 🔐 Security

- ✅ Production-ready Django settings
- ✅ HTTPS enabled
- ✅ Security headers configured
- ✅ CSRF protection
- ✅ Environment variables for secrets
- ✅ SQLite in dev, ready for PostgreSQL in prod

---

## 📝 Features

### Current Features

- ✅ Service exploration
- ✅ Enquiry management
- ✅ Article/Blog posts
- ✅ Event management
- ✅ Feedback collection
- ✅ Admin dashboard
- ✅ Chat widget

### Admin Panel

Access at: https://ai-solutions1.onrender.com/admin-login

---

## 🐛 Troubleshooting

### Local Issues

```bash
# Clear Python cache
find . -type d -name __pycache__ -exec rm -r {} +

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Reset database
rm db.sqlite3
python manage.py migrate
```

### Deployment Issues

See [DEPLOYMENT.md - Troubleshooting Section](DEPLOYMENT.md#-troubleshooting)

---

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete deployment guide
- **[Django Docs](https://docs.djangoproject.com/)** - Django documentation
- **[Render Docs](https://render.com/docs)** - Render documentation

---

## 👤 Author

- **Developer**: Sabanam Poudel
- **Repository**: https://github.com/SabanamPoudel/Ai-Solutions1
- **Website**: https://ai-solutions1.onrender.com

---

## 📜 License

This project is provided as-is for educational purposes.

---

## 🔗 Links

- 🌐 Live Website: https://ai-solutions1.onrender.com
- 📚 Deployment Guide: See DEPLOYMENT.md
- 💻 GitHub: https://github.com/SabanamPoudel/Ai-Solutions1
- 📧 For support: Check project documentation

---

**Last Updated**: July 3, 2026
