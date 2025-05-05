from fastapi import APIRouter, Depends
from app import schemas, auth
from sqlalchemy.orm import Session
from app.auth import get_db

router = APIRouter(prefix="/bmi", tags=["bmi"])

@router.post("/calculate", response_model=schemas.BMIRecordOut)
def calc_bmi(r: schemas.BMIRecordCreate, db: Session = Depends(get_db),
             current: auth.models.User = Depends(auth.get_current_user)):
    # аналогично create_record, но без записи в БД
    bmi = r.weight / (r.height ** 2)
    cat = ("underweight" if bmi<18.5 else
           "normal"      if bmi<25  else
           "overweight"  if bmi<30  else
           "obese")
    # можем возвращать единоразовую сущность без id и created_at
    return {
        "id": 0,
        "user_id": current.id,
        "weight": r.weight,
        "height": r.height,
        "bmi": bmi,
        "category": cat,
        "created_at": None
    }