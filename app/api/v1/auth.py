from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordRequestForm
from supabase import Client
from app.database import get_db
from app.schemas.admin import AdminOut
from app.core.auth import verify_password, create_access_token, get_current_admin
from app.core.config import settings
from jose import JWTError, jwt
from app.schemas.admin import TokenData

router = APIRouter()

def get_admin_from_cookie(request: Request, db: Client = Depends(get_db)):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Not authenticated")
        token_data = TokenData(email=email)
    except JWTError:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    response = db.table("admins").select("*").eq("email", token_data.email).execute()
    admin = response.data[0] if response.data else None
    
    if admin is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return admin

@router.post("/login")
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Client = Depends(get_db)):
    res = db.table("admins").select("*").eq("email", form_data.username).execute()
    admin = res.data[0] if res.data else None
    
    if not admin or not verify_password(form_data.password, admin.get("hashed_password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": admin.get("email")}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        path="/"
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=AdminOut)
def read_users_me(current_admin: dict = Depends(get_admin_from_cookie)):
    return current_admin
