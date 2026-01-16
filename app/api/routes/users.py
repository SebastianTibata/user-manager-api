from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.models.user import User, UserCreateIn, UserUpdate
from app.db.database import engine



router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

def get_db():
    with Session(engine) as session:
        yield session

#Obtener todos los usuarios
@router.get("/")
def get_users(db : Session = Depends(get_db)):
    statement = select(User)
    users = db.exec(statement).all()
    return users

#Obtener un usuario por id 
@router.get("/{id}")
def get_user_by_id(id : int, db: Session = Depends(get_db)):
    statement = select(User)
    users = db.exec(statement).all()
    for user in users:
        if user.id == id:
            content = user.model_dump()
            return JSONResponse(content, status_code=200)
    return {}


#Crear Usuarios
@router.post("/")
def create_user(
    user_in: UserCreateIn,
    db : Session = Depends(get_db)
):
    user = User(
        name=user_in.name,
        edad=user_in.edad,
        email=user_in.email
    )
    
    existing_user = db.exec(
        select(User).where(User.email == user_in.email)
    ).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail = "El email ya esta registrado")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

#Modificar Usuario
@router.put("/{id}")
def update_user(
    id:int, 
    user_in : UserUpdate, 
    db:Session = Depends(get_db) 
):
    user = db.get(User,id)
    
    if not user:
        raise HTTPException(status_code= 400, detail="Usuario no encontrado")
    
    #Obtener Solo los datos que el cliente envió
    update_data = user_in.model_dump(exclude_unset= True)
    
    #Asignar valores a cada variable
    for field, value in update_data.items():
        setattr(user,field,value)
        
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

#Eliminar usuario
@router.delete("/{id}")
def delete_user(
    id: int,
    db:Session = Depends(get_db)
):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(user)
    db.commit()
    
    return "Usuario borrado con exito"