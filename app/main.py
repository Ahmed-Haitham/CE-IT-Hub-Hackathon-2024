# app/main.py

import asyncio

from typing import Optional
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.crud import SymptomClient, DiseaseGroupClient, BigTableClient

from .models import Base, OneBigTable
from .db import engine, get_session, start_db

app = FastAPI(title="WUM Neurological disease tool backend")

#This won't be required in production, as the db will be persistent
@app.on_event("startup")
async def startup_event():
    await start_db(engine)

@app.get("/")
async def root():
    return {"message": "See /docs or /redoc for the API documentation"}

@app.get("/symptoms", response_model=list[schemas.SymptomBigTable])
async def list_symptoms(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.list_symptoms(search_for)

@app.get("/symptoms/{symptom}", response_model=schemas.SymptomBigTable)
async def get_symptom(symptom_name: str, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.get_symptom(symptom_name)

@app.get("/diseaseGroups", response_model=list[schemas.DiseaseGroupBigTable])
async def list_disease_groups(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.list_disease_groups(search_for)

@app.get("/diseaseGroups/{disease_group}", response_model=schemas.DiseaseGroupBigTable)
async def get_disease_group(disease_group: str, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.get_disease_group(disease_group)

@app.get('/bigTable', response_model=list[schemas.FullBigTable])# here there is an issue with the schema of the response 
async def list_table_entries(db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.list_table_entries()

@app.get('/bigTable/{entry_id}', response_model=schemas.FullBigTable)
async def get_table_entry(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.get_table_entry(table_entry_id)

@app.post('/bigTable', response_model=schemas.FullBigTable)
async def post_table_entry(table_entry: schemas.BaseBigTable, db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.add_entry(table_entry)
