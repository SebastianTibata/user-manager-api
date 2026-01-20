from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.schemas.user import UserCreateIn, UserUpdate, UserCreateOut
from app.db.database import get_db
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserCreateOut])
def get_users(db: Session = Depends(get_db)):
    return user_service.get_users(db)

@router.get("/{id}", response_model=UserCreateOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    user = user_service.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/",response_model=UserCreateOut)
def create_user(user_in: UserCreateIn, db: Session = Depends(get_db)):
    try:
        return user_service.create_user(db, user_in)
    except ValueError as e:
        if str(e) == "EMAIL_EXISTS":
            raise HTTPException(status_code=400, detail="El email ya está registrado")

@router.put("/{id}", response_model=UserCreateOut)
def update_user(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    try:
        return user_service.update_user(db, id, user_in)
    except ValueError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

@router.delete("/{id}", status_code= 204)
def delete_user(id: int, db: Session = Depends(get_db)):
    try:
        user_service.delete_user(db, id)
        return {"detail": "Usuario borrado con éxito"}
    except ValueError:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
