# app/main.py

import asyncio

from typing import Optional
from fastapi import FastAPI, Depends, Query
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
async def list_symptoms(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.list_symptoms(search_for)

@app.get("/symptoms/{symptom_id}", response_model=schemas.ReadSymptom)
async def get_symptom(symptom_id: int, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.get_symptom(symptom_id)

@app.post("/symptoms", response_model=schemas.ReadSymptom)
async def create_symptom(symptom: schemas.CreateSymptom, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.create_symptom(symptom)

@app.get("/diseaseGroups", response_model=list[schemas.ReadDiseaseGroup])
async def list_disease_groups(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.list_disease_groups(search_for)

@app.get("/diseaseGroups/{disease_group_id}", response_model=schemas.ReadDiseaseGroup)
async def get_disease_group(disease_group: int, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.get_disease_group(disease_group)

@app.post("/diseaseGroups", response_model=schemas.ReadDiseaseGroup)
async def create_disease_group(disease_group: schemas.CreateDiseaseGroup, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.create_disease_group(disease_group)