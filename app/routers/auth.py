from fastapi import APIRouter,status,Depends,responses,HTTPException
from sqlalchemy.orm import Session
from .. import database,utils,model,oauth2
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])

@router.post("/login")
def login_user(User_credentials:OAuth2PasswordRequestForm = Depends() , db:Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == User_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_304_NOT_MODIFIED , detail="Invalid credentials")
    if not utils.verify_password(User_credentials.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid credentials")
    access_token = oauth2.create_access_token(
        data={'user_id':user.id ,},
        expires_delta= timedelta(minutes=oauth2.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"eccess_token":access_token , "token_type":"bearer"}
