# URL Shortener with Click Analytics

A fast, lightweight URL Shortening service built with **Python**, **FastAPI**, and **SQLite**. Supports custom aliases, Base62-style random short code generation, HTTP 307 redirection, and real-time click tracking.

## Features
- **Custom & Auto-Generated Aliases:** Shorten long URLs into 6-character alphanumeric codes or custom branded aliases.
- **Database Indexing:** Uses SQLite with an indexed `short_code` column for fast O(log N) lookup speeds.
- **Click Analytics:** Tracks total redirect hits and creation timestamps per shortened URL.
- **Automated Testing:** Includes end-to-end integration tests with `pytest`.

## Tech Stack
- **Language:** Python 3
- **Framework:** FastAPI, Uvicorn
- **Database:** SQLite3
- **Testing:** Pytest, HTTPX

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/shorten` | Accepts a long URL (and optional `custom_alias`) and returns a short URL. |
| `GET` | `/{short_code}` | Redirects to the original URL and increments the click counter. |
| `GET` | `/api/stats/{short_code}` | Returns click analytics and metadata for a given short code. |

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone https://github.com
   cd url-shortener-analytics
   ```
2. Activate virtual environment & install dependencies:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```
4. Open `http://127.0.0` in your browser to test via Swagger UI.
