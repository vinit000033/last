import os
import uuid
from datetime import datetime
from flask import request
from werkzeug.utils import secure_filename
from app import app, db
from models import BookAnalytics, ClickEvent

def save_file(file, subfolder):
    """
    Save an uploaded file to the specified subfolder
    Returns the path relative to the static folder
    """
    filename = secure_filename(file.filename)
    # Add unique identifier to filename to prevent overwriting
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    
    # Create subfolder if it doesn't exist
    upload_path = os.path.join(app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_path, exist_ok=True)
    
    # Save the file
    file_path = os.path.join(upload_path, unique_filename)
    file.save(file_path)
    
    # Return the path relative to static folder
    return os.path.join('uploads', subfolder, unique_filename)

def delete_file(file_path):
    """
    Delete a file from the file system
    """
    try:
        if file_path and os.path.exists(os.path.join('static', file_path)):
            os.remove(os.path.join('static', file_path))
            return True
    except Exception as e:
        app.logger.error(f"Error deleting file: {e}")
    return False

def increment_analytics(book_id, event_type):
    """
    Increment analytics counters for a book and record click event
    """
    try:
        # Get or create analytics record
        analytics = BookAnalytics.query.filter_by(book_id=book_id).first()
        if not analytics:
            analytics = BookAnalytics(book_id=book_id)
            db.session.add(analytics)
        
        # Update the appropriate counter
        if event_type == 'view':
            analytics.view_count += 1
        elif event_type == 'download':
            analytics.download_count += 1
        elif event_type == 'share':
            analytics.share_count += 1
        
        # Record the click event
        click_event = ClickEvent(
            book_id=book_id,
            event_type=event_type,
            user_agent=request.user_agent.string,
            ip_address=request.remote_addr,
            referrer=request.referrer
        )
        db.session.add(click_event)
        
        # Commit changes
        db.session.commit()
        return True
    except Exception as e:
        app.logger.error(f"Error recording analytics: {e}")
        db.session.rollback()
        return False
