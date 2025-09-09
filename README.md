# URL Shortener (FastAPI)

Paste a long link and get a short one you can share. Includes a tiny UI, redirects, and basic stats.

## Why this app (simple)

- **Short links are easier to share** in chats, SMS, slides, and print.
- **Cleaner to read** than long URLs with lots of `?utm_...` stuff.
- **Better QR codes:** shorter text → simpler codes that scan more easily.
- **You stay in control:** your domain, your redirects, your stats.

## Features
- `POST /api/shorten` → returns `{ code, short_url, original_url }`
- `GET /{code}` → redirects and increments `hit_count`
- `GET /api/stats/{code}` → returns `{ code, original_url, created_at_utc, hit_count }`
- Minimal UI at `/` to create and copy links
- Input validation and duplicate detection (same long URL → same code)
- In-memory storage for now (simple and fast for local dev)

## Tech Stack
- Python, FastAPI, Uvicorn
- HTML/CSS/vanilla JS (static page)
- In-memory store (SQLite planned next)

## Project Structure
```bash
app/
  __init__.py
  main.py              # API routes + static hosting
  schemas.py           # request/response models
  db/
    __init__.py
    memory.py          # in-memory store (hit counts, etc.)
  utils/
    __init__.py
    codes.py           # secure Base62 code generator
static/
  index.html           # tiny UI to call the API
.gitignore
README.md
requirements.txt
```

## Prerequisites
- **Python** 3.10+ and **pip**
- (Optional) **VS Code** with the **Python** extension
- This repo’s `requirements.txt` (FastAPI, Uvicorn, etc.)

---

## Setup
1) **Clone & open** the repo in your editor.  
2) **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```
3) **Activate the virtual environment**:
    a) **Windows**
        ```bash
        .venv\Scripts\activate
        ```
