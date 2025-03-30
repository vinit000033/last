from app import db
from models import User
from werkzeug.security import generate_password_hash

def create_admin_user(username, email, password):
    """Create an admin user with the provided credentials"""
    try:
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            print(f"Admin user '{username}' already exists.")
            return True
        
        # Create new admin user
        admin_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"Admin user '{username}' created successfully!")
        return True
    
    except Exception as e:
        print(f"Error creating admin user: {str(e)}")
        return False