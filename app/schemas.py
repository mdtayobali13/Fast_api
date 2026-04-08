from pydantic import BaseModel ,HttpUrl,EmailStr
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CourseCreate(BaseModel):
    name: str
    instructor: str
    duration: float
    website: HttpUrl


class CourseResponse(CourseCreate):
    id : int
    creator_id : int
    class config:
        orm_model =True


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    instructor: Optional[str] = None
    duration: Optional[int] = None
    website: Optional[str] = None

    

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserResponse(BaseModel):
    id : int
    email:EmailStr
    created_at: datetime
    
    class config:
        orrm_model = True





class UserLogin(BaseModel):
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None