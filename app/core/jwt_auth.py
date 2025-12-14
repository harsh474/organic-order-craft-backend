from datetime import datetime, timedelta
from jose import jwt, JWTError
from app.config.settings import settings
import redis
from fastapi import Request, Depends, HTTPException, status

redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

JWT_COOKIE_NAME = "ghee_jwt"

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")
        # Check if token is blacklisted in Redis
        if jti and redis_client.get(f"bl_jti:{jti}"):
            raise JWTError("Token is revoked")
        return payload
    except JWTError:
        return None

def set_jwt_cookie(response, token):
    response.set_cookie(
        key=JWT_COOKIE_NAME,
        value=token,
        # httponly=True,
        secure=False,
        samesite="lax",
        path="/"
    )

def get_token_from_request(request: Request):
    return request.cookies.get(JWT_COOKIE_NAME)

def revoke_token(token: str, expire_seconds: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        jti = payload.get("jti")
        if jti:
            redis_client.setex(f"bl_jti:{jti}", expire_seconds, 1)
    except JWTError:
        pass

# Dependency for FastAPI - get current user_id from JWT cookie
from fastapi import Request, HTTPException, status

def get_current_user_id(request: Request):
    token = get_token_from_request(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authentication cookie")
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    return int(payload["sub"])
