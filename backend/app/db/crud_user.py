from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..schemas.user import UserCreate
from ..utils.security import hash_password

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user(db: Session, user_id):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_in: UserCreate):
    hashed = hash_password(user_in.password)
    user = User(email=user_in.email, password_hash=hashed, full_name=user_in.full_name, role=user_in.role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
