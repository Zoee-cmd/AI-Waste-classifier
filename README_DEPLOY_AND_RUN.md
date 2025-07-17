# EcoSort (GREEN CITY HACK) - Local Run & Deployment Guide

## 🚀 How to Run Locally (Windows Command Prompt)

### 1. Open Command Prompt
- Press `Windows + R`, type `cmd`, and press Enter.

### 2. Navigate to the Django App Directory
```cmd
cd "C:\Users\USER\Downloads\Ubuntu Conference\django_app"
```

### 3. (Optional) Create a Virtual Environment
```cmd
python -m venv venv
venv\Scripts\activate
```

### 4. Install Requirements
```cmd
pip install -r requirements.txt
```

### 5. Run Database Migrations
```cmd
python manage.py migrate
```

### 6. Collect Static Files
```cmd
python manage.py collectstatic --noinput
```

### 7. Run the Django Development Server
```cmd
python manage.py runserver
```

### 8. Open in Your Browser
- Go to: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🌍 How to Deploy (Railway or Render)

### 🚦 Railway (Recommended)
1. Go to [https://railway.app/](https://railway.app/) and sign up.
2. Click **New Project** → **Deploy from GitHub repo** (or upload your code).
3. Railway auto-detects Django. If not, set the start command to:
   ```bash
   gunicorn ecosort.wsgi
   ```
4. Add a PostgreSQL plugin if you need a database.
5. Click **Deploy**. Railway will build and give you a public URL.

### 🚦 Render
1. Go to [https://render.com/](https://render.com/) and sign up.
2. Click **New Web Service**.
3. Connect your GitHub repo.
4. Set build command:
   ```bash
   pip install -r requirements.txt
   ```
5. Set start command:
   ```bash
   gunicorn ecosort.wsgi
   ```
6. Add environment variables as needed (e.g., `DJANGO_SECRET_KEY`).
7. Deploy and get a public URL.

---

## 📝 Troubleshooting
- **Module not found?**
  ```cmd
  pip install -r requirements.txt
  ```
- **Port in use?**
  ```cmd
  python manage.py runserver 8080
  ```
- **Static files not showing?**
  ```cmd
  python manage.py collectstatic --noinput
  ```
- **Database errors?**
  ```cmd
  python manage.py migrate
  ```

---

## 🗂️ Project Structure (Key Files)
- `manage.py` — Django project manager
- `requirements.txt` — Python dependencies
- `Procfile` — For deployment (should contain: `web: gunicorn ecosort.wsgi`)
- `ecosort/` — Django project settings
- `waste_classifier/` — Main app
- `static/` and `templates/` — Static files and HTML templates

---

## 💡 Tips
- Always activate your virtual environment before running commands.
- Use `Ctrl+C` to stop the server.
- For deployment, make sure your `ALLOWED_HOSTS` in `settings.py` is set to `['*']` or your deployment URL.

---

**Enjoy using EcoSort (GREEN CITY HACK)!** 