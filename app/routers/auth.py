from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlmodel import Session
from app.schemas.user import UserCreate, UserRead, UserLogin, UserUpdate
from app.services.auth import create_user, authenticate_user, get_user_by_email, update_user_profile
from app.models.user import User
from app.config.settings import settings
from app.core.database import get_session
from app.core.jwt_auth import create_access_token, set_jwt_cookie, get_current_user_id, get_token_from_request, revoke_token
import uuid
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "*"
]

router = APIRouter(prefix="/auth", tags=["auth"])

# Signup
@router.post("/signup")
def signup(user_in: UserCreate, response: Response, session: Session = Depends(get_session)): 
    print("signup api is called++++++++++++++++",response)
    if get_user_by_email(session, user_in.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    user = create_user(
        session,
        email=user_in.email,
        password=user_in.password,
        phone=user_in.phone,
        address=user_in.address
    )
    jti = str(uuid.uuid4())
    token = create_access_token({"sub": str(user.id), "jti": jti})
    set_jwt_cookie(response, token)
    return {"user":user}

# Login
@router.post("/login")
def login(user_in: UserLogin, response: Response, session: Session = Depends(get_session)):
    user = authenticate_user(session, user_in.email, user_in.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    jti = str(uuid.uuid4())
    token = create_access_token({"sub": str(user.id), "jti": jti})
    set_jwt_cookie(response, token)
    return {"success": True, "message": "Login successful","user":user}

# Logout
@router.post("/logout")
def logout(response: Response, request: Request):
    token = get_token_from_request(request)
    if token:
        revoke_token(token)
    response.delete_cookie(key="ghee_jwt")
    return {"success": True, "message": "Logout successful"}

# Get current user (profile)
@router.get("/me")
def get_me(user_id: int = Depends(get_current_user_id), session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user":user}



# Update profile (only phone/address)
@router.patch("/me", response_model=UserRead)
def update_me(
    update_in: UserUpdate,
    user_id: int = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    user = update_user_profile(session, user_id, update_in.phone, update_in.address)
    return user
