from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, models, auth

router = APIRouter(prefix="/profiles", tags=["profiles"])

@router.post("/", response_model=schemas.ProfileOut)
def create_profile(p: schemas.ProfileCreate, db: Session = Depends(auth.get_db), 
                   current: models.User = Depends(auth.get_current_user)):
    if current.profile:
        raise HTTPException(400, "Profile already exists")
    prof = models.Profile(**p.dict(), user_id=current.id)
    db.add(prof); db.commit(); db.refresh(prof)
    return prof

@router.get("/", response_model=schemas.ProfileOut)
def read_profile(db: Session = Depends(auth.get_db), current: models.User = Depends(auth.get_current_user)):
    if not current.profile:
        raise HTTPException(404, "Profile not found")
    return current.profile

@router.put("/", response_model=schemas.ProfileOut)
def update_profile(p: schemas.ProfileCreate, db: Session = Depends(auth.get_db), 
                   current: models.User = Depends(auth.get_current_user)):
    prof = current.profile
    if not prof:
        raise HTTPException(404, "Profile not found")
    for k,v in p.dict().items():
        setattr(prof, k, v)
    db.commit(); db.refresh(prof)
    return prof

@router.delete("/", status_code=204)
def delete_profile(db: Session = Depends(auth.get_db), current: models.User = Depends(auth.get_current_user)):
    prof = current.profile
    if not prof:
        raise HTTPException(404, "Profile not found")
    db.delete(prof); db.commit()