# Kaku - Waitlist Application

This repository contains the Kaku waitlist application. It is split into a static frontend and a Django backend.

## Architecture

- **Frontend**: A static HTML/CSS/JS landing page built for Netlify. It uses `index.html` to present a beautiful, animated landing page.
- **Backend**: A Django application (`/backend`) with a native PostgreSQL database connection. It exposes REST APIs for the waitlist and provides a secure admin dashboard.

## Quick Start (Backend)

The backend is located in the `backend/` directory.

### Requirements
- Python 3.10+
- A PostgreSQL database (for production) or SQLite (for local dev)

### Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
3. Fill in your `DATABASE_URL` in the `.env` file (leave empty to use local SQLite).
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run migrations (this creates Django's auth tables; the waitlist table is managed externally):
   ```bash
   python manage.py migrate
   ```
6. Create an admin user:
   ```bash
   python manage.py createsuperuser
   ```
7. Start the server:
   ```bash
   python manage.py runserver
   ```

### Admin Dashboard
Access the secure admin dashboard by navigating to:
`http://localhost:8000/dashboard/`

Login with the superuser credentials you created. From there, you can view waitlist stats, search users, export to CSV, and send broadcast emails.

## Quick Start (Frontend)

The frontend is in the root directory (`index.html`).

1. Make sure your backend is running (e.g., on port 8000).
2. Open `index.html` in your browser or serve it with a local web server (e.g., `python -m http.server`).
3. You can configure the `API_URL` within the `<script>` tag in `index.html` (search for `CONFIG.API_URL`) to point to your backend.

## Deployment

- **Frontend**: Deploy the root folder to Netlify, Vercel, or GitHub Pages.
- **Backend**: Deploy the `backend/` folder to a service like Render, Heroku, or Railway. See `backend/DEPLOYMENT.md` for detailed instructions.
