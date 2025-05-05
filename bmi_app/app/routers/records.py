from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models, auth

router = APIRouter(prefix="/records", tags=["records"])

@router.post("/", response_model=schemas.BMIRecordOut)
def create_record(
    r: schemas.BMIRecordCreate,
    db: Session = Depends(auth.get_db),
    current: models.User = Depends(auth.get_current_user),
):
    # правильный расчёт BMI
    bmi = r.weight / (r.height ** 2)
    if bmi < 18.5:
        cat = "underweight"
    elif bmi < 25:
        cat = "normal"
    elif bmi < 30:
        cat = "overweight"
    else:
        cat = "obese"

    rec = models.BMIRecord(
        user_id=current.id,
        weight=r.weight,
        height=r.height,
        bmi=bmi,
        category=cat,
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@router.get("/", response_model=List[schemas.BMIRecordOut])
def list_records(
    db: Session = Depends(auth.get_db),
    current: models.User = Depends(auth.get_current_user),
):
    return db.query(models.BMIRecord).filter_by(user_id=current.id).all()

@router.get("/{record_id}", response_model=schemas.BMIRecordOut)
def get_record(
    record_id: int,
    db: Session = Depends(auth.get_db),
    current: models.User = Depends(auth.get_current_user),
):
    rec = (
        db.query(models.BMIRecord)
        .filter_by(id=record_id, user_id=current.id)
        .first()
    )
    if not rec:
        raise HTTPException(404, "Record not found")
    return rec

@router.put("/{record_id}", response_model=schemas.BMIRecordOut)
def update_record(
    record_id: int,
    r: schemas.BMIRecordCreate,
    db: Session = Depends(auth.get_db),
    current: models.User = Depends(auth.get_current_user),
):
    rec = (
        db.query(models.BMIRecord)
        .filter_by(id=record_id, user_id=current.id)
        .first()
    )
    if not rec:
        raise HTTPException(404, "Record not found")

    # пересчёт при обновлении
    rec.weight = r.weight
    rec.height = r.height
    rec.bmi = r.weight / (r.height ** 2)
    rec.category = (
        "underweight"
        if rec.bmi < 18.5
        else "normal"
        if rec.bmi < 25
        else "overweight"
        if rec.bmi < 30
        else "obese"
    )
    db.commit()
    db.refresh(rec)
    return rec

@router.delete("/{record_id}", status_code=204)
def delete_record(
    record_id: int,
    db: Session = Depends(auth.get_db),
    current: models.User = Depends(auth.get_current_user),
):
    rec = (
        db.query(models.BMIRecord)
        .filter_by(id=record_id, user_id=current.id)
        .first()
    )
    if not rec:
        raise HTTPException(404, "Record not found")
    db.delete(rec)
    db.commit()