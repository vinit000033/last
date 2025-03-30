from app import app, db
from models import Book, BookAnalytics
from datetime import datetime

with app.app_context():
    # Check if any books exist
    book_count = Book.query.count()
    
    if book_count == 0:
        # Create a sample book
        book = Book(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            description="The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, the novel depicts narrator Nick Carraway's interactions with mysterious millionaire Jay Gatsby and Gatsby's obsession to reunite with his former lover, Daisy Buchanan.",
            publisher="Charles Scribner's Sons",
            year=1925,
            isbn="9780743273565",
            category="fiction",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add to database
        db.session.add(book)
        db.session.commit()
        
        # Create analytics entry for the book
        analytics = BookAnalytics(
            book_id=book.id,
            view_count=0,
            download_count=0,
            share_count=0,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        db.session.add(analytics)
        db.session.commit()
        
        print("Sample book created successfully!")
    else:
        print("Books already exist in the database.")