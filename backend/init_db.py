"""
Database initialization script
Creates default user for MVP
"""
from app.db import SessionLocal, init_db
from app.db.models import User


def create_default_user():
    """Create default user for MVP (user_id = 1)"""
    db = SessionLocal()
    try:
        # Check if user exists
        existing_user = db.query(User).filter(User.id == 1).first()
        if existing_user:
            print("Default user already exists")
            return
        
        # Create default user
        user = User(
            email="demo@fanecho.com",
            username="demo_user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Created default user: {user.username} (ID: {user.id})")
    
    except Exception as e:
        print(f"Error creating default user: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Creating default user...")
    create_default_user()
    print("Database initialization complete!")
