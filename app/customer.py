from . import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from .database import get_db
from datetime import datetime
from .auth.auth_bearer import JWTBearer

router = APIRouter()

# [...] get all recordsCustId
@router.get('/', dependencies=[Depends(JWTBearer())])
def get_customers(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str = ''):
    skip = (page - 1) * limit

    cust = db.query(models.Customers).filter(
        models.Customers.name.contains(search)).limit(limit).offset(skip).all()
    return {'status': 'success', 'results': len(cust), 'customers': cust}

# [...] create record
@router.post('/', status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def create_customer(payload: schemas.CustBaseSchema, db: Session = Depends(get_db)):
    new_cust = models.Customers(**payload.dict())
    db.add(new_cust)
    db.commit()
    db.refresh(new_cust)
    return {"status": "success", "customer": new_cust}

# [...] edit record
@router.patch('/{CustId}', dependencies=[Depends(JWTBearer())])
def update_customer(CustId: str, payload: schemas.CustUpdBaseSchema, db: Session = Depends(get_db)):
    cust_query = db.query(models.Customers).filter(models.Customers.id == CustId)
    db_cust = cust_query.first()

    if not db_cust:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No customer with this id: {CustId} found')
    update_data = payload.dict(exclude_unset=True)
    cust_query.filter(models.Customers.id == CustId).update(update_data,
                                                       synchronize_session=False)
    db.commit()
    db.refresh(db_cust)
    return {"status": "success", "customer": db_cust}

# [...] get single record
@router.get('/{CustId}', dependencies=[Depends(JWTBearer())])
def get_customer(CustId: str, db: Session = Depends(get_db)):
    cust = db.query(models.Customers).filter(models.Customers.id == CustId).first()
    if not cust:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No customer with this id: {CustId} found")
    return {"status": "success", "customer": cust}

@router.delete('/{CustId}', dependencies=[Depends(JWTBearer())])
def delete_customer(CustId: str, db: Session = Depends(get_db)):
    cust_query = db.query(models.Customers).filter(models.Customers.id == CustId)
    cust = cust_query.first()
    if not cust:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No cust with this id: {CustId} found')
    cust_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
