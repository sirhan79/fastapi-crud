from app import models, customer, user
from fastapi import FastAPI
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router, tags=['Users'], prefix='/api/users')
app.include_router(customer.router, tags=['Customers'], prefix='/api/customers')

@app.get("/api/healthchecker")
def root():
    return {"message": "Welcome to FastAPI with SQLAlchemy"}
