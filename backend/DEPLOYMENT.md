# Kaku Backend Deployment Guide

This project is a Django backend that connects to a PostgreSQL database (or local SQLite) and serves API endpoints for a waitlist, alongside a custom Django Admin Dashboard.

## Prerequisites

- Python 3.10+
- PostgreSQL connection string (for production)
- Optional: SMTP Server credentials (SendGrid, Resend, etc.) for emails

## Environment Setup

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Fill in the variables:
   - `DATABASE_URL`: Your PostgreSQL connection string. Leave blank for local SQLite.
   - `SECRET_KEY`: A secure random string for Django.
   - `DEBUG`: Set to `False` for production.
   - Email settings (if you want to send emails).

## Local Development

1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Or `venv\Scripts\activate` on Windows
   pip install -r requirements.txt
   ```

2. Run the server:
   ```bash
   python manage.py migrate
   python manage.py runserver

3. Create an admin user for the dashboard:
   ```bash
   python manage.py createsuperuser
   ```

## Production Deployment (Render, Heroku, Railway, etc.)

1. **Connect Repository**: Connect your Git repository to your chosen platform.
2. **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
3. **Start Command**: `gunicorn config.wsgi:application`
4. **Environment Variables**: Add all the variables from your `.env` file to your hosting platform's environment settings.

### Static Files
The project uses `whitenoise` to serve static files efficiently in production. `collectstatic` will place them in the `staticfiles` directory.

### CORS
If your frontend is hosted on a specific domain (e.g., Netlify), update `CORS_ALLOWED_ORIGINS` in `settings.py` (or via a new env var) to restrict access to your API. Currently, `CORS_ALLOW_ALL_ORIGINS = True` for ease of setup.
