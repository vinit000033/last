from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    # Check if admin user already exists
    admin_user = User.query.filter_by(username='admin').first()
    
    if not admin_user:
        # Create admin user
        admin = User(
            username='admin',
            email='admin@library.com',
            is_admin=True
        )
        admin.password_hash = generate_password_hash('admin123')
        
        # Add to database
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully!")
    else:
        print("Admin user already exists!")