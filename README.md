# AQUANET Survey — Setup Guide

## Quick Start

### 1. Install dependencies
```bash
pip install flask
```

### 2. Run the app
```bash
cd aquanet_survey
python app.py
```

### 3. Open in browser
- **Survey form:** http://localhost:5000
- **Admin panel:** http://localhost:5000/admin
- **Export CSV:**  http://localhost:5000/admin/export

---

## Deploy Online (Free Options)

### Option A — Render.com (Recommended, Free)
1. Push this folder to a GitHub repo
2. Go to https://render.com → New Web Service
3. Connect your repo
4. Set **Build Command:** `pip install -r requirements.txt`
5. Set **Start Command:** `python app.py`
6. Deploy → get a public URL like `https://aquanet-survey.onrender.com`

### Option B — Railway.app
1. Push to GitHub
2. Go to https://railway.app → New Project → Deploy from GitHub
3. It auto-detects Flask and deploys

### Option C — PythonAnywhere (Free tier)
1. Sign up at https://www.pythonanywhere.com
2. Upload files via dashboard
3. Create a new web app → Flask → point to app.py

---

## File Structure
```
aquanet_survey/
├── app.py               ← Flask backend + SQLite logic
├── requirements.txt     ← Dependencies
├── survey.db            ← Auto-created on first run
└── templates/
    ├── survey.html      ← Beautiful survey form (20 questions)
    ├── thankyou.html    ← Success page after submission
    └── admin.html       ← View all responses table
```

## Pages
| URL | Description |
|-----|-------------|
| `/` | Survey form |
| `/submit` | POST handler (auto-redirect) |
| `/thankyou` | Confirmation page |
| `/admin` | View all responses |
| `/admin/export` | Download responses as CSV |
