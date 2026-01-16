from sqlmodel import SQLModel, Field
from typing import Optional


class UserBase(SQLModel):
    name: str = Field()
    edad: int = Field()
    email: str = Field()

class UserUpdate(SQLModel):
    name: Optional[str] = None
    edad: Optional[int] = None
    email: Optional[str] = None    
    
class UserCreateIn(UserBase): ...
    
class UserCreateOut(UserBase,SQLModel):
    id: int = Field()
    
class User(UserBase, table = True):
    id : int | None  = Field (default = None, primary_key= True)
    