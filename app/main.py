# app/main.py

from fastapi import FastAPI, Depends

from app import schemas
from app import crud

from .models import Base, Symptom, DiseaseGroup
from .db import SessionLocal, engine

#This creates the tables in the database
Base.metadata.create_all(bind=engine)
app = FastAPI(title="WUM Neurological disease tool backend")

#Other functions depend on this one to get a session via fastapi's dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/symptoms", response_model=list[schemas.Symptom])
def list_symptoms(db = Depends(get_db)):
    return crud.list_symptoms(db)
