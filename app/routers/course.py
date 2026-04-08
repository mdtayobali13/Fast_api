from fastapi import FastAPI, status , HTTPException , Depends , APIRouter
from sqlalchemy.orm import Session
from .. import model , schemas 
from ..database import get_db
from typing import List, Optional
from .. import oauth2

router = APIRouter(
    prefix="/course",
    tags=["courses"]
)

@router.get("/" , response_model= List[schemas.CourseResponse])
def view_course(db:Session = Depends(get_db), current_user : model.User = Depends(oauth2.get_current_user) , limit :int = 6 , skip:int=0 ,search: Optional[str]=""):
    # courses = db.query(model.Course).all()
    courses = db.query(model.Course).filter(model.Course.creator_id == current_user.id).filter(model.Course.name.contains(search)).limit(limit).offset(skip).all()
    return courses




@router.get("/{id}" , response_model= schemas.CourseResponse)
def view_course(id:int, db:Session=Depends(get_db),current_user : model.User = Depends(oauth2.get_current_user)):
    courses = db.query(model.Course).filter(model.Course.id == id).first()

    if not courses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail= f"Course with id : {id} was not found")
    if courses.creator_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN , 
            detail="Not authorized action"
        )
    return courses



@router.post("/",response_model=schemas.CourseResponse)
def create_course(post:schemas.CourseCreate , db : Session = Depends(get_db),current_user : model.User = Depends(oauth2.get_current_user)):
    new_courses = model.Course(**post.model_dump(), creator_id = current_user.id)

    new_courses.website = str(post.website)

    db.add(new_courses)
    db.commit()
    db.refresh(new_courses)
    return new_courses



@router.put("/{id}", response_model=schemas.CourseResponse)
def update_course(
    id: int, 
    updated_course: schemas.CourseCreate, 
    db: Session = Depends(get_db),
    current_user: model.User = Depends(oauth2.get_current_user)
):
    course = db.query(model.Course).filter(model.Course.id == id).first()
    if not course:
        raise HTTPException(status_code=404, detail=f"Course with id {id} not found")
    if course.creator_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this course")
    update_data = updated_course.model_dump()
    update_data.pop("creator_id", None)
    if "website" in update_data:
        update_data["website"] = str(update_data["website"])
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@router.patch("/{id}", response_model=schemas.CourseResponse)
def update_course(id: int, updated_course: schemas.CourseUpdate, db: Session = Depends(get_db), current_user: model.User = Depends(oauth2.get_current_user)):
    course = db.query(model.Course).filter(model.Course.id == id).first()
    update_data = updated_course.model_dump(exclude_unset=True)
    update_data.pop("creator_id", None) 
    for key, value in update_data.items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course


@router.delete("/{id}" , status_code=status.HTTP_200_OK)
def delete_course(id:int , db:Session = Depends(get_db),current_user : model.User = Depends(oauth2.get_current_user)):
    deleted_course = db.query(model.Course).filter(model.Course.id == id).first()

    if not deleted_course :
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND
        )
    if deleted_course.creator_id != current_user.id :
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN , 
            detail="Not authorized action"
        )
    
    db.delete(deleted_course)
    db.commit()
    return {"details":f"Course with id:{id} has been deleted"}