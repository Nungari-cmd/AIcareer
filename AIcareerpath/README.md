# CareerAI — Full-Stack Flask + Claude App

AI-powered career path decision maker. Students fill in their skills and goals;
Flask calls the Anthropic API securely on the server side and returns personalised
career paths, course recommendations, and a 12-month roadmap.

---

## Project Structure

```
career-ai/
├── app.py               ← Flask backend (API route + server)
├── requirements.txt     ← Python dependencies
├── .env                 ← Your secret API key (never commit this)
├── .gitignore
└── templates/
    └── index.html       ← Frontend (served by Flask)
```

---

## Setup & Run (5 steps)

### 1. Make sure Python is installed
```bash
python --version   # needs 3.8+
```

### 2. Create and activate a virtual environment
```bash
# Create venv
python -m venv venv

# Activate — Mac/Linux:
source venv/bin/activate

# Activate — Windows:
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Anthropic API key
Open the `.env` file and replace the placeholder:
```
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxxxxxxxxxx
```
Get your key at: https://console.anthropic.com/

### 5. Run the app
```bash
python app.py
```

Then open your browser at → **http://localhost:5000**

---

## How it works

```
Browser (index.html)
    │  POST /api/analyse  { profile data, no API key }
    ▼
Flask (app.py)
    │  Reads ANTHROPIC_API_KEY from .env
    │  Calls https://api.anthropic.com/v1/messages
    ▼
Claude API
    │  Returns career analysis as JSON
    ▼
Flask
    │  Parses + validates JSON, forwards to browser
    ▼
Browser
    Renders career paths, courses, skills, roadmap
```

The API key **never leaves the server** — the browser only talks to `/api/analyse`.

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ANTHROPIC_API_KEY is not set` | Check your `.env` file |
| `ModuleNotFoundError: flask` | Run `pip install -r requirements.txt` |
| Page not loading | Make sure you ran `python app.py` and visit `http://localhost:5000` |
| API timeout | Try again — Claude usually responds in 5–15 seconds |
