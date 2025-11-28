from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import Author, Book
from pydantic import BaseModel
from typing import List

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library CRUD API", version="1.0")

# Pydantic schemas (for request/response)
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

# ---------- AUTHOR CRUD ----------
@app.post("/authors/", response_model=AuthorResponse)
def create_author(author: AuthorCreate, db: Session = Depends(get_db)):
    db_author = Author(name=author.name)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
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
    db.commit()
    db.refresh(db_author)
    return db_author

@app.delete("/authors/{author_id}", response_model=dict)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    author = db.get(Author, author_id)
    if not author:
        raise HTTPException(404, "Author not found")
    db.delete(author)
    db.commit()
    return {"message": "Author deleted"}

# ---------- BOOK CRUD ----------
@app.post("/books/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(title=book.title, author_id=book.author_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return {
        "id": db_book.id,
        "title": db_book.title,
        "author_id": db_book.author_id,
        "author_name": db_book.author.name
    }

@app.get("/books/", response_model=List[BookResponse])
def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [{"id": b.id, "title": b.title, "author_id": b.author_id, "author_name": b.author.name} for b in books]

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    return {"id": book.id, "title": book.title, "author_id": book.author_id, "author_name": book.author.name}

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: BookCreate, db: Session = Depends(get_db)):
    db_book = db.get(Book, book_id)
    if not db_book:
        raise HTTPException(404, "Book not found")
    db_book.title = book.title
    db_book.author_id = book.author_id
    db.commit()
    db.refresh(db_book)
    return {"id": db_book.id, "title": db_book.title, "author_id": db_book.author_id, "author_name": db_book.author.name}

@app.delete("/books/{book_id}", response_model=dict)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if not book:
        raise HTTPException(404, "Book not found")
    db.delete(book)
    db.commit()
    return {"message": "Book deleted"}