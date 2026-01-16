from fastapi import FastAPI, Depends
from app.api.routes import auth,tasks,users
from sqlmodel import SQLModel
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models import user


app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.get('/')
def home():
    return 'Hi'
@app.get("/db")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def read_root(db: Session = Depends(get_db)):
    return {"mensaje": "Conectado a PostgreSQL 🚀"}


app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(users.router)
