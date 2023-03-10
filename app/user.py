from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db
from datetime import datetime
from .auth.auth_handler import hash_password, signJWT, verify_password
from .auth.auth_bearer import JWTBearer

router = APIRouter()

# [...] create record
@router.post('/', status_code=status.HTTP_201_CREATED)
def create_user(payload: schemas.UserBaseSchema, db: Session = Depends(get_db)):
    new_user = models.Users(**payload.dict())
    new_user.password = hash_password(new_user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #return {"status": "success", "user": new_user}
    return {"status": "success", "user": new_user, "token": signJWT(new_user.email)}

@router.delete('/{UserId}', dependencies=[Depends(JWTBearer())])
def delete_user(UserId: str, db: Session = Depends(get_db)):
    user_query = db.query(models.Users).filter(models.Users.id == UserId)
    usr = user_query.first()
    if not usr:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No user with this id: {UserId} found')
    user_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.post("/login")
async def user_login(user: schemas.UserLoginSchema, db: Session = Depends(get_db)):
    #usr = db.query(models.Users).filter((models.Users.email == user.email) & (models.Users.password == hash_password(user.password))).first()
    usr = db.query(models.Users).filter(models.Users.email == user.email).first()
    
    if (usr and verify_password(user.password, usr.password)):
        return signJWT(user.email)
        #return {"status": "success", "customer": usr, "Token":signJWT(user.password)}
    return {
        "error": "Wrong login details!"
    }
