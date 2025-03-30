import os
import uuid
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, send_from_directory, jsonify, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from app import app, db
from models import User, Book, BookAnalytics, ClickEvent
from forms import LoginForm, BookForm
from utils import save_file, delete_file, increment_analytics

# Index/Home route
@app.route('/')
def index():
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('index.html', title='Digital Library', books=books, now=datetime.now())

# Book detail route
@app.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    # Record view event
    increment_analytics(book_id, 'view')
    return render_template('book_detail.html', title=book.title, book=book, now=datetime.now())

# Download book route
@app.route('/book/<int:book_id>/download')
def download_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Record download event
    increment_analytics(book_id, 'download')
    
    # Check if the book has a direct file or external URL
    if book.file_path:
        # Get the filename from the file_path
        filename = os.path.basename(book.file_path)
        filepath = os.path.join('static', book.file_path)
        directory = os.path.dirname(filepath)
        return send_from_directory(directory=directory, path=filename, as_attachment=True)
    elif book.book_url:
        # Redirect to external URL
        return redirect(book.book_url)
    else:
        flash('This book is not available for download.', 'error')
        return redirect(url_for('book_detail', book_id=book_id))

# Share book API route
@app.route('/api/book/<int:book_id>/share', methods=['POST'])
def share_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Record share event
    increment_analytics(book_id, 'share')
    
    return jsonify({'success': True, 'message': 'Share recorded'})

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data) and user.is_admin:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html', title='Admin Login', form=form, now=datetime.now())

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

# Admin dashboard route
@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        abort(403)
    
    total_books = Book.query.count()
    total_views = db.session.query(db.func.sum(BookAnalytics.view_count)).scalar() or 0
    total_downloads = db.session.query(db.func.sum(BookAnalytics.download_count)).scalar() or 0
    
    recent_books = Book.query.order_by(Book.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                          title='Admin Dashboard',
                          total_books=total_books,
                          total_views=total_views,
                          total_downloads=total_downloads,
                          recent_books=recent_books,
                          now=datetime.now())

# Admin manage books route
@app.route('/admin/books')
@login_required
def manage_books():
    if not current_user.is_admin:
        abort(403)
    
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('admin/manage_books.html', title='Manage Books', books=books, now=datetime.now())

# Admin add book route
@app.route('/admin/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not current_user.is_admin:
        abort(403)
    
    form = BookForm()
    if form.validate_on_submit():
        # Create the book
        book = Book(
            title=form.title.data,
            author=form.author.data,
            description=form.description.data,
            publisher=form.publisher.data,
            year=form.year.data,
            isbn=form.isbn.data,
            category=form.category.data,
            book_url=form.book_url.data
        )
        
        # Handle cover image upload
        if form.cover.data:
            cover_path = save_file(form.cover.data, 'covers')
            book.cover_path = cover_path
        
        # Handle book file upload
        if form.book_file.data:
            file_path = save_file(form.book_file.data, 'books')
            book.file_path = file_path
        
        # Save to database
        db.session.add(book)
        db.session.commit()
        
        # Create analytics entry
        analytics = BookAnalytics(book_id=book.id)
        db.session.add(analytics)
        db.session.commit()
        
        flash('Book added successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('admin/add_book.html', title='Add Book', form=form, now=datetime.now())

# Admin edit book route
@app.route('/admin/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    if not current_user.is_admin:
        abort(403)
    
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        # Update book details
        book.title = form.title.data
        book.author = form.author.data
        book.description = form.description.data
        book.publisher = form.publisher.data
        book.year = form.year.data
        book.isbn = form.isbn.data
        book.category = form.category.data
        book.book_url = form.book_url.data
        
        # Handle cover image upload
        if form.cover.data:
            # Delete old cover if exists
            if book.cover_path:
                delete_file(book.cover_path)
            
            cover_path = save_file(form.cover.data, 'covers')
            book.cover_path = cover_path
        
        # Handle book file upload
        if form.book_file.data:
            # Delete old file if exists
            if book.file_path:
                delete_file(book.file_path)
            
            file_path = save_file(form.book_file.data, 'books')
            book.file_path = file_path
        
        # Update timestamp
        book.updated_at = datetime.utcnow()
        
        # Save to database
        db.session.commit()
        
        flash('Book updated successfully!', 'success')
        return redirect(url_for('manage_books'))
    
    return render_template('admin/edit_book.html', title='Edit Book', form=form, book=book, now=datetime.now())

# Admin delete book route
@app.route('/admin/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    if not current_user.is_admin:
        abort(403)
    
    book = Book.query.get_or_404(book_id)
    
    # Delete associated files
    if book.cover_path:
        delete_file(book.cover_path)
    
    if book.file_path:
        delete_file(book.file_path)
    
    # Delete analytics data
    BookAnalytics.query.filter_by(book_id=book.id).delete()
    ClickEvent.query.filter_by(book_id=book.id).delete()
    
    # Delete book
    db.session.delete(book)
    db.session.commit()
    
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('manage_books'))

# Admin analytics route
@app.route('/admin/analytics')
@login_required
def admin_analytics():
    if not current_user.is_admin:
        abort(403)
    
    books = Book.query.join(BookAnalytics).all()
    
    # Get daily click data for the past 30 days
    thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
    daily_clicks = ClickEvent.query.filter(ClickEvent.timestamp >= thirty_days_ago).all()
    
    return render_template('admin/analytics.html', 
                          title='Analytics Dashboard',
                          books=books,
                          daily_clicks=daily_clicks,
                          now=datetime.now(),
                          date_today=datetime.utcnow(),
                          timedelta=timedelta)

# API route for tracking events
@app.route('/api/track', methods=['POST'])
def track_event():
    data = request.json
    book_id = data.get('book_id')
    event_type = data.get('event_type')
    
    if not book_id or not event_type:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Check if book exists
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'error': 'Book not found'}), 404
    
    # Record the event
    success = increment_analytics(book_id, event_type)
    
    if success:
        return jsonify({'success': True})
    else:
        return jsonify({'error': 'Failed to record event'}), 500
