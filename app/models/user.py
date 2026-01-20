from sqlmodel import SQLModel, Field
from typing import Optional

    
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    edad: int = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
