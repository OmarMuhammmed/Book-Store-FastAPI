from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    body = Column(String, nullable=False)
    rating = Column(Integer)

    book_id = Column(Integer, ForeignKey('books.id'))
    book = relationship("Book", back_populates="reviews")
