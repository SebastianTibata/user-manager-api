from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from typing import Optional

class UserBase(SQLModel):
    name: str = Field(min_length=2, max_length=20)
    edad: int = Field(gt=0,lt=120)
    email: EmailStr

class UserUpdate(SQLModel):
    name: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[EmailStr] = None    
    
class UserCreateIn(UserBase): 
    @field_validator("name")
    def no_numeros(cls,v):
        if any(char.isdigit() for char in v):
            raise ValueError("El nombre no puede contener números")
        return v
    
class UserCreateOut(SQLModel):
    id: int = Field()
    name : str
    edad : int
    email : EmailStr