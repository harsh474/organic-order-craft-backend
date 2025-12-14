from sqlmodel import Session, select
from app.models.user import User
from passlib.context import CryptContext
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    print("HASH INPUT LENGTH:", len(password))
    return password
    # return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    # print("VERIFY INPUT LENGTH:", len(plain_password.encode()))
    return pwd_context.verify(plain_password, hashed_password)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email) 
    
    user = session.exec(statement).first() 
    print("user in get_user_by_email++++++++++++",user)
    return user

def create_user(session: Session, email: str, password: str, phone: str, address: Optional[str] = None) -> User:
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, phone=phone, address=address)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(session, email) 
    
    if not user :
    # or not verify_password(password, user.hashed_password):
        return None
    return user



def update_user_profile(session: Session, user_id: int, phone: Optional[str], address: Optional[str]) -> User:
    user = session.get(User, user_id)
    if not user:
        raise ValueError("User not found")
    if phone:
        user.phone = phone
    if address is not None:  # address can be blank
        user.address = address
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
