from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException,
    status
)
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional

from core.database import get_db
from models.book import Book
from schemas.book import (
    BookCreateSchema,
    BookResponseSchema,
    BookUpdateSchema,
)

router = APIRouter(prefix='/api/books')


def get_book_by_id(book_id: int, db: Session) -> Book:
    """Get book by ID or raise 404 if not found"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found!')
    return book


def build_search_query(query, search: str):
    """Build search filter for books query"""
    return query.filter(
        or_(
            Book.title.ilike(f"%{search}%"),
            Book.description.ilike(f"%{search}%")
        )
    )


@router.get('/', response_model=List[BookResponseSchema])
def list_books(
    search: Optional[str] = Query(None, description="Search by title or description"),
    order_by: Optional[str] = Query('id', pattern='^-?(title|id)$', description="Order by title or id"),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if search:
        query = build_search_query(query, search)

    if order_by == 'title':
        query = query.order_by(Book.title)
    elif order_by == '-title':
        query = query.order_by(Book.title.desc())
    elif order_by == '-id':
        query = query.order_by(Book.id.desc())
    else:
        query = query.order_by(Book.id)

    return query.all()


@router.post('/', response_model=BookResponseSchema, status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get('/{book_id}', response_model=BookResponseSchema)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return get_book_by_id(book_id, db)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    db.delete(book)
    db.commit()


@router.put('/{book_id}', response_model=BookResponseSchema)
def update_book(book_id: int, book_update: BookUpdateSchema, db: Session = Depends(get_db)):
    book = get_book_by_id(book_id, db)
    
    update_data = book_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book
