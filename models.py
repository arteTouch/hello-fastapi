from pydantic import BaseModel, validator, Field, EmailStr
from typing import Optional, List

class CustomBaseModel(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1)
    
class User(CustomBaseModel):
    email: EmailStr

class Category(CustomBaseModel):
    pass

class Task(CustomBaseModel):
    description: Optional[str] = Field('Does not contain any description', min_length=10)
    is_active: bool = Field(is_bool=True)
    user: User
    category: Category
    tags: Optional[List[str]] = []
