# app/main.py

import asyncio

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import SymptomClient, DiseaseGroupClient, AssocSymptomDiseaseGroupClient

from .models import Base, Symptom, DiseaseGroup
from .db import engine, get_session, start_db

app = FastAPI(title="WUM Neurological disease tool backend")

#This won't be required in production, as the db will be persistent
@app.on_event("startup")
async def startup_event():
    await start_db(engine)

@app.get("/")
async def root():
    return {"message": "See /docs or /redoc for the API documentation"}

@app.get("/symptoms", response_model=list[schemas.ReadSymptom])
async def list_symptoms(db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.list_symptoms()

@app.post("/symptoms", response_model=schemas.ReadSymptom)
async def create_symptom(symptom: schemas.CreateSymptom, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.create_symptom(symptom)