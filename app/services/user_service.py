from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreateIn, UserUpdate, UserCreateOut

# Obtener usuarios
def get_users(db: Session) -> list[UserCreateOut]:
    return db.exec(select(User)).all()

# Obtener Usuario por id
def get_user_by_id(db: Session, user_id: int) -> UserCreateOut | None:
    return db.get(User, user_id)

#Crear usuario
def create_user(db: Session, user_in: UserCreateIn) -> UserCreateOut:
    existing_user = db.exec(
        select(User).where(User.email == user_in.email)
    ).first()

    if existing_user:
        raise ValueError("EMAIL_EXISTS")

    user = User(**user_in.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Modificar usuario
def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    user = db.get(User, user_id)
    if not user:
        raise ValueError("USER_NOT_FOUND")

    for field, value in user_in.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Eliminar Usuario
def delete_user(db: Session, user_id: int) -> None:
    user = db.get(User, user_id)
    if not user:
        raise ValueError("USER_NOT_FOUND")

    db.delete(user)
    db.commit()
