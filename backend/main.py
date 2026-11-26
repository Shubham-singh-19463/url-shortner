from datetime import datetime
from fastapi import FastAPI, Path, HTTPException
from imp_function import generate_short_code
from dotenv import load_dotenv
import os
from sqlalchemy import String, create_engine, select, text, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from model import URLCreate
from fastapi.responses import RedirectResponse, HTMLResponse
from pathlib import Path as FilePath
from fastapi.middleware.cors import CORSMiddleware


# read url from env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not configured")

# connection to postgresql database student_db
engine = create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

class UrlShortner(Base):
    __tablename__ = "url_data"
    id : Mapped[int] = mapped_column(primary_key=True)
    original_url : Mapped[str] = mapped_column()
    short_url : Mapped[str] = mapped_column(String(20), unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now()
)

Base.metadata.create_all(bind=engine)  
SessionLocal = sessionmaker(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://url-shortner-frontend-bice.vercel.app/"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "This is url shortner api"}

@app.get("/url/{url}")
def open_link(url : str = Path(...)):
    
    try:
        with SessionLocal() as session:
            statement = select(UrlShortner).where(UrlShortner.short_url == url)
            students = session.scalars(statement).first()
            
            if students is None:
                html = FilePath(r"../frontend/404.html").read_text(encoding="utf-8")
                return HTMLResponse(
                    content=html,
                    status_code=404
                )
                
            return RedirectResponse(students.original_url,status_code=307)


    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Server error"
        )
        
# fix error of short url duplicate
@app.post("/url", status_code=201)
def shorten_link(url: URLCreate):

    origin_url = str(url.original_url)
    short_url = generate_short_code()
    

    url_data = UrlShortner(
        original_url=origin_url,
        short_url=short_url
    )

    try:
        with SessionLocal() as session:
            session.add(url_data)
            session.commit()
            session.refresh(url_data)

            return {
                "original_url": url_data.original_url,
                "short_url": url_data.short_url,
                "created_at": url_data.created_at
            }

    except IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="Error in generating url"
        )

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )
    

