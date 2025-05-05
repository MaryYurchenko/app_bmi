from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, auth
from app.database import SessionLocal, init_db

router = APIRouter(prefix="/auth", tags=["auth"])

# удаляем тут вызов init_db() — он уже происходит в main.py

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(400, "Username already registered")
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(400, "Email already registered")
    hashed = auth.get_password_hash(user_in.password)
    user = models.User(username=user_in.username, email=user_in.email, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: schemas.UserCreate, db: Session = Depends(auth.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(401, "Incorrect username or password")
    token = auth.create_access_token({"sub": user.id})
    return {"access_token": token}
