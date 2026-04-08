from fastapi import FastAPI, status , HTTPException , Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model , schemas , utils
from ..database import get_db


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post('', status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def course_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    if db.query(model.User).filter(model.User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists"
        )

    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password

    new_user = model.User(**user.model_dump())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user