from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional, List

class CustomBaseModel(BaseModel):
    name: str = Field(min_length=1)
    
class User(CustomBaseModel):
    email: EmailStr

class Category(CustomBaseModel):
    priority: str = Field(min_length=1)

class Task(CustomBaseModel):
    description: Optional[str] = Field('Does not contain any description', min_length=10)
    is_active: bool = Field(True, is_bool=True)
    user: str = Field('655fd6e9ee7e0fdc320bfde5', min_length=1)
    category: str = Field(min_length=1)
