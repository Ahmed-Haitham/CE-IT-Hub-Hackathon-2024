# app/main.py

import asyncio

from typing import Optional
from fastapi import FastAPI, Depends, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from io import BytesIO
from app import schemas
from app.crud import SymptomClient, DiseaseGroupClient, SymmetricityClient, ProgressionClient, OnsetGroupClient, BigTableClient, TestCkLevelClient

from .models import Base, OneBigTable
from .db import engine, get_session, start_db
from .handlers.file_input_handler import read_xlsx_and_load_to_tables
import pandas as pd

app = FastAPI(title="WUM Neurological disease tool backend")

#This won't be required in production, as the db will be persistent
@app.on_event("startup")
async def startup_event():
    await start_db(engine)

@app.get("/")
async def root():
    return {"message": "See /docs or /redoc for the API documentation"}

@app.get("/symptoms", response_model=list[schemas.FullSymptoms])
async def list_symptoms(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.list_symptoms(search_for)

@app.get("/symptoms/{symptom_id}", response_model=schemas.FullSymptoms)
async def get_symptom(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.get_symptom(table_entry_id)

@app.post('/symptoms', response_model=schemas.FullSymptoms)
async def post_table_entry(table_entry: schemas.BaseSymptoms, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.add_symptom(table_entry)

@app.get("/diseaseGroups", response_model=list[schemas.FullDiseaseGroup])
async def list_disease_groups(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.list_disease_groups(search_for)

@app.get("/diseaseGroups/{disease_group_id}", response_model=schemas.FullDiseaseGroup)
async def get_disease_group(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.get_disease_group(table_entry_id)

@app.get("/symmetricity", response_model=list[schemas.FullSymmetricity])
async def list_symmetricities(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymmetricityClient(db)
    return await client.list_symmetricities(search_for)

@app.get("/symmetricity/{symmetricity_id}", response_model=schemas.FullSymmetricity)
async def get_symmetricity(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = SymmetricityClient(db)
    return await client.get_symmetricity(table_entry_id)

@app.get("/progression", response_model=list[schemas.FullProgression])
async def list_progressions(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = ProgressionClient(db)
    return await client.list_progressions(search_for)

@app.get("/progression/{progression_id}", response_model=schemas.FullProgression)
async def get_progression(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = ProgressionClient(db)
    return await client.get_progression(table_entry_id)

@app.get("/onset_group", response_model=list[schemas.FullOnsetGroup])
async def list_onset_groups(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = OnsetGroupClient(db)
    return await client.list_onset_groups(search_for)

@app.get("/onset_group/{onset_group_id}", response_model=schemas.FullOnsetGroup)
async def get_onset_group(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = OnsetGroupClient(db)
    return await client.get_onset_group(table_entry_id)

@app.get("/test_ck_level", response_model=list[schemas.FullTestCkLevel])
async def list_test_ck_levels(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = TestCkLevelClient(db)
    return await client.list_test_ck_levels(search_for)

@app.get("/test_ck_level/{test_ck_level_id}", response_model=schemas.FullTestCkLevel)
async def test_ck_level(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = TestCkLevelClient(db)
    return await client.test_ck_level(table_entry_id)

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


@app.post("/uploadfile/", response_model=dict)
async def create_upload_file(file: UploadFile, db: AsyncSession = Depends(get_session)):
    contents = file.file.read()
    buffer = BytesIO(contents)
    await read_xlsx_and_load_to_tables(buffer, db)
    df = pd.read_excel(buffer)
    buffer.close()
    file.file.close()

    # statement = select(models.DiseaseGroup).filter(models.DiseaseGroup.id == disease_group_id)
    #     result =  await _execute_statement(self.session, statement)
    #     return result.first()

    # async def create_disease_group(self, disease_group: schemas.CreateDiseaseGroup):
    # new_disease_group = models.DiseaseGroup(**disease_group.model_dump())
    # self.session.add(new_disease_group)
    # await self.session.commit()
    # await self.session.refresh(new_disease_group)
    # return new_disease_group

    return {"filename": file.filename, "columns": df.columns.to_list()}
