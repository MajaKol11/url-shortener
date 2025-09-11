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
    - **Windows**
        ```bash
        .venv\Scripts\activate
        ```
    - **macOS/Linux**
        ```bash
        source .venv/bin/activate
        ```
4) **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Run Locally 
- Start the server (auto reloads on code changes): 
 ```bash
  uvicorn app.main:app --reload
  ```
- Open http://127.0.0.1:8000 for the UI.
- Open http://127.0.0.1:8000/docs for the interactive API docs (Swagger UI)
- Health check: http://127.0.0.1:8000/health
- **Note**: This build uses in-memory storage. All data resets when the server restarts.

## Usage
**UI**
1) Visit `/` 
2) Paste a full http or https URL
3) Click Shorten - copy or open the returned short link
**API**
- Create a short link
```bash
  curl -X POST http://127.0.0.1:8000/api/shorten \
    -H "Content-Type: application/json" \
    -d '{"url":"https://example.com/docs?q=1#top"}'
```
- Response (example)
```json
  {
  "code": "A1b2C3d4",
  "short_url": "http://127.0.0.1:8000/A1b2C3d4",
  "original_url": "https://example.com/docs?q=1#top"
  }
```
- Follow a short link
 `http://127.0.0.1:8000/A1b2C3d4`
- Get stats for a code
```bash
 curl http://127.0.0.1:8000/api/stats/A1b2C3d4
 ```
- Response (example)
```json
  {
  "code": "A1b2C3d4",
  "original_url": "https://example.com/docs?q=1#top",
  "created_at_utc": "2025-09-09T12:00:00.000000+00:00",
  "hit_count": 3
  }
```
 
 ## Troubleshooting
 **422 or 400 errors when shortening:**
 - Ensure the body is valid JSON: `{"url":"https://..."}`
 - Only **absolute** `http` / `https` URLs are allowed
 - Max URL length: 2048 characters
 **404 on `/api/stats/{code}` or  `/{code}`:**
 - The code doesn't exist (create it first via `POST /api/shorten`)
 - Remember: in-memory store clears on server restart
 **Nothing happens on `/`:**
 - Check the server logs for errors
 - Ensure `static/index.html` exists and the app is serving it at `/`.

 ## Common Tasks
 - **Change server port (e.g 9000)**
 - ```bash
   uvicorn app.main:app --reload --port 9000
   ```
- **Run without reload**
- ```bash
  uvicorn app.main:app
  ```


