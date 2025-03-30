import os
import sys
from app import app, db
import models  # Import all models to ensure they're registered

def setup_database():
    """Initialize the database tables"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("Database tables created successfully!")

def run_admin_setup():
    """Run the admin setup script"""
    from setup_railway_admin import create_admin_user
    
    username = os.environ.get('ADMIN_USERNAME', 'railway_admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@railway.app')
    password = os.environ.get('ADMIN_PASSWORD')
    
    if not password:
        print("ERROR: No admin password provided. Set ADMIN_PASSWORD environment variable.")
        return False
    
    with app.app_context():
        success = create_admin_user(username, email, password)
    return success

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "all"
    
    if action in ["all", "db"]:
        setup_database()
    
    if action in ["all", "admin"]:
        run_admin_setup()
    
    print("Railway setup completed!")