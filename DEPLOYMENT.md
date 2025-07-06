# 🚀 Deployment Guide for Creative Blog

This document outlines the steps to deploy the **Creative Blog** Django project to a production environment.

---

## 📁 Project Structure (Important Files)

creative_blog/
├── blog/
├── users/
├── adminpanel/
├── media/
├── static/
├── env/ # virtual environment (excluded from Git)
├── .env ✅ environment variables (secret)
├── .gitignore
├── manage.py
├── requirements.txt ✅ dependencies
├── DEPLOYMENT.md ✅ this file

---

## ✅ Prerequisites

- Python 3.10 or later
- `pip` package manager
- A production server (e.g. **Render**, **Heroku**, **VPS**, or **Docker**)
- A domain (optional)
- PostgreSQL (optional but recommended)

---

## 🔐 Environment Variables (`.env`)

Create a `.env` file and add this content (example):

SECRET_KEY=your_production_secret_key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,127.0.0.1

---

## 📦 Install Dependencies

```bash
pip install -r requirements.txt

⚙️ Collect Static Files
python manage.py collectstatic

🛠️ Migrate the Database
python manage.py makemigrations
python manage.py migrate

👤 Create Superuser (optional)
python manage.py createsuperuser

🌐 Allowed Hosts (in .env)
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

🔒 Recommended Security Settings (in settings.py)
SECURE_HSTS_SECONDS = 31536000
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

☁ Deployment Platform Options
Option 1: Render (Free Hosting)
Add your GitHub repo

Use Gunicorn:
pip install gunicorn

Add this to Render "Start Command":
gunicorn creative_blog.wsgi:application

Option 2: Heroku
heroku create
heroku config:set SECRET_KEY=your_key
heroku config:set DEBUG=False
git push heroku main

Option 3: PythonAnywhere
Upload project from GitHub

Set WSGI path to creative_blog.wsgi.application

Set env variables in Web tab

✅ Final Checklist
 Login/logout works?

 Admin panel secure?

 Blog posts display correctly?

 Media & static files work?

 Comments, Likes, Bookmarks functional?

 Emails send (if setup)?

🧠 Final Notes
Back up the database

Don’t share .env or SECRET_KEY

Monitor logs

Update dependencies regularly


---

### 🔹 3. Done ✅

Your project is now **documented for deployment**.

---

Would you like help deploying on **Render**, **PythonAnywhere**, or generating your `requirements.txt` next?
```
