from fastapi import (
    APIRouter,
    Depends,
    Query,
    HTTPException
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


@router.get('/', response_model=List[BookResponseSchema])
def list_book(
    search: Optional[str] = Query(
        None, description="Search by title or description"),
    order_by: Optional[str] = Query(
        'id', pattern='^-?(title|id)$', description="Order by title or id"),
    db: Session = Depends(get_db)
):
    query = db.query(Book)

    if search:
        query = query.filter(
            or_(
                Book.title.ilike(f"%{search}%"),
                Book.description.ilike(f"%{search}%")
            )
        )

    if order_by == 'title':
        query = query.order_by(Book.title)

    elif order_by == '-title':
        query = query.order_by(Book.title.desc())

    elif order_by == '-id':
        qurey = query.order_by(Book.id.desc())

    else:
        query = query.order_by(Book.id)

    books = query.all()
    return books


@router.post('/', response_model=BookResponseSchema)
def create_book(book: BookCreateSchema, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get('/{book_id}', response_model=BookResponseSchema)
def book_detail(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found!')
    return book


@router.delete('/{book_id}', status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found!')

    db.delete(book)
    db.commit()

    return {"message": "Book Deleted Successfully !"}


@router.put('/{book_id}', response_model=BookResponseSchema, status_code=200)
def update_book(book_id: int,
                book_update: BookUpdateSchema,
                db: Session = Depends(get_db)
                ):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail='Book not found!')

    updated_data = book_update.model_dump()
    for key, value in updated_data.items():
        setattr(book, key, value)

       # print(f"{key}:{value}") To DEBUG

    db.commit()
    db.refresh(book)
    return book
