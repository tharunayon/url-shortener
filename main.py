from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from models import URL
from schemas import URLCreate, URLResponse
from utils import generate_short_code
from config import settings

# Initialize database schemas
Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener API")
templates = Jinja2Templates(directory="templates")
templates.env.cache = None
@app.get("/", response_class=HTMLResponse)
def render_homepage(request: Request):
    """Serves the clean user-facing HTML frontend."""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/shorten", response_model=URLResponse, status_code=status.HTTP_201_CREATED)
def shorten_url(url_in: URLCreate, db: Session = Depends(get_db)):
    original_url_str = str(url_in.original_url)
    
    existing_url = db.query(URL).filter(URL.original_url == original_url_str).first()
    if existing_url:
        return URLResponse(
            original_url=existing_url.original_url,
            short_url=f"{settings.BASE_URL}/{existing_url.short_code}",
            short_code=existing_url.short_code,
            clicks=existing_url.clicks
        )
    
    for _ in range(10):
        short_code = generate_short_code()
        collision_check = db.query(URL).filter(URL.short_code == short_code).first()
        if not collision_check:
            break
    else:
        raise HTTPException(status_code=500, detail="Could not create unique short code.")
        
    db_url = URL(original_url=original_url_str, short_code=short_code)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    
    return URLResponse(
        original_url=db_url.original_url,
        short_url=f"{settings.BASE_URL}/{db_url.short_code}",
        short_code=db_url.short_code,
        clicks=db_url.clicks
    )

@app.get("/{short_code}")
def redirect_to_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URL).filter(URL.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
        
    db_url.clicks += 1
    db.commit()
    return RedirectResponse(url=db_url.original_url)
