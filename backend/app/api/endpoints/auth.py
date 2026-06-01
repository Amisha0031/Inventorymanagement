from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.user import User as UserSchema, UserCreate
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core import security, config
from app.schemas.token import Token
from app.models.user import User as UserModel



router = APIRouter()

@router.post("/login", response_model=Token)
def login_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=access_token_expires),
        "token_type": "bearer",
    }


@router.post('/register', response_model=UserSchema)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user_in.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed_password = security.get_password_hash(user_in.password)
    db_user = UserModel(email=user_in.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
