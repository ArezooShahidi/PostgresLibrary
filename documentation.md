# Library Management System – PostgreSQL + SQLAlchemy + FastAPI (Full CRUD with Swagger UI)

A clean, production-ready Python library project using:
- PostgreSQL (via Docker)
- SQLAlchemy 2.0+ (ORM)
- FastAPI (automatic Swagger UI at `/docs`)

## Project Structure
```
postgreslib/
├── .venv/
├── __init__.py                  # Makes directory a Python package
├── database.py                  # SQLAlchemy engine & session handling
├── models.py                    # ORM models (Author ↔ Book)
├── main.py                      # Full FastAPI CRUD API + Swagger
├── docker-compose.yml
└── requirements.txt (optional)
```

## Step-by-Step Setup

### 1. Create and Activate Virtual Environment
```bash
python -m venv .venv
.\.venv\Scripts\activate    # Windows
# source .venv/bin/activate # macOS/Linux
```

### 2. Start PostgreSQL with Docker
**`docker-compose.yml`**
```yaml
version: '3.8'
services:
  db:
    image: postgres:16
    restart: always
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: library
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

Run:
```bash
docker-compose up -d
```

### 3. Install Dependencies
```bash
pip install sqlalchemy psycopg2-binary fastapi uvicorn pydantic
```

### 4. `database.py` – Database Engine & Session
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://user:password@localhost:5432/library"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### 5. `models.py` – ORM Models
```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    books = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
```

### 6. `main.py` – Full CRUD API with FastAPI & Swagger UI
```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Author, Book
from pydantic import BaseModel
from typing import List

# Create tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Library Management API",
    description="Complete CRUD operations for Authors and Books",
    version="2.0"
)

# Pydantic schemas
class AuthorCreate(BaseModel):
    name: str

class AuthorResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

class BookCreate(BaseModel):
    title: str
    author_id: int

class BookResponse(BaseModel):
    id: int
    title: str
    author_id: int
    author_name: str
    class Config:
        from_attributes = True

# ====================== AUTHOR CRUD ======================
@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author); db.commit(); db.refresh(db_author)
    return db_author

@app.get("/authors/", response_model=List[AuthorResponse])
def read_authors(db: Session = Depends(get_db)):
    return db.query(Author).all()

@app.get("/authors/{author_id}", response_model=AuthorResponse)
def read_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(404, "Author not found")
    return author

@app.put("/authors/{author_id}", response_model=AuthorResponse)
def update_author(author_id: int, author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = db.get(Author, author_id)
    if not db_author:
        raise HTTPException(404, "Author not found")
    db_author.name = author.name
    db.commit(); db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(404, "Author not found")
    db.delete(author); db.commit()
    return {"message": "Author deleted successfully"}

# ====================== BOOK CRUD ======================
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author_id=book.author_id)
    db.add(db_book); db.commit(); db.refresh(db_book)
    return {
        "id": db_book.id,
        "title": db_book.title,
        "author_id": db_book.author_id,
        "author_name": db_book.author.name
    }

@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "author_id": b.author_id,
            "author_name": b.author.name
        } for b in books
    ]

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return {
        "id": book.id,
        "title": book.title,
        "author_id": book.author_id,
        "author_name": book.author.name
    }

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.get(Book, book_id)
    if not db_book:
        raise HTTPException(404, "Book not found")
    db_book.title = book.title
    db_book.author_id = book.author_id
    db.commit(); db.refresh(db_book)
    return {
        "id": db_book.id,
        "title": db_book.title,
        "author_id": db_book.author_id,
        "author_name": db_book.author.name
    }

@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book); db.commit()
    return {"message": "Book deleted successfully"}
```

### 7. Run the API
```bash
uvicorn main:app --reload
```

### 8. Access Interactive Documentation
- **Swagger UI**: http://127.0.0.1:8000/docs  
- **ReDoc**: http://127.0.0.1:8000/redoc

All endpoints are fully interactive – test CREATE, READ, UPDATE, DELETE directly in the browser.
