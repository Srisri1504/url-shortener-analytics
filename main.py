import string
import random
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from database import init_db, create_short_url, get_url_and_increment, get_url_stats

app = FastAPI(title="URL Shortener with Click Analytics")

@app.on_event("startup")
def startup_event():
    init_db()

class URLRequest(BaseModel):
    url: HttpUrl
    custom_alias: str | None = None

def generate_short_code(length: int = 6) -> str:
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))

@app.post("/api/shorten")
def shorten_url(payload: URLRequest, request: Request):
    original_url = str(payload.url)
    
    if payload.custom_alias:
        short_code = payload.custom_alias.strip()
        if not create_short_url(short_code, original_url):
            raise HTTPException(status_code=400, detail="Custom alias already in use.")
    else:
        for _ in range(5):
            short_code = generate_short_code()
            if create_short_url(short_code, original_url):
                break
        else:
            raise HTTPException(status_code=500, detail="Could not generate unique short code.")

    base_url = str(request.base_url).rstrip("/")
    return {
        "short_code": short_code,
        "short_url": f"{base_url}/{short_code}",
        "original_url": original_url
    }

@app.get("/api/stats/{short_code}")
def url_analytics(short_code: str):
    record = get_url_stats(short_code)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    return {
        "short_code": record["short_code"],
        "original_url": record["original_url"],
        "total_clicks": record["clicks"],
        "created_at": record["created_at"]
    }

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    record = get_url_and_increment(short_code)
    if not record:
        raise HTTPException(status_code=404, detail="Short URL not found.")
    return RedirectResponse(url=record["original_url"], status_code=307)
