# app/main.py

import os
from io import BytesIO

import pandas as pd
from fastapi import Depends, FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.auth import (
    JWTBearer,
)
from app.crud import (
    AuthClient,
    BigTableClient,
    PredictionClient,
    SymptomDefinitionsClient,
    DiseaseGroupDefinitionsClient,
    SymptomsClient
)
from app.db import AsyncSessionFactory, engine, get_session, start_db

from .utils.data_loader import read_xlsx_and_load_to_tables

app = FastAPI(title="WUM Neurological disease tool backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#This won't be required in production, as the db will be persistent
@app.on_event("startup")
async def startup_event():
    await start_db(engine)
    try:
        db = AsyncSessionFactory()
        client = AuthClient(db)
        current_users = await client.get_users()
        ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME")
        ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

        if ADMIN_USERNAME not in [user["username"] for user in current_users]:
            user = schemas.UserModel(username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
            await client.add_user(user=user)
    finally:
        await db.close()


@app.get("/")
async def root():
    return {"message": "See /docs or /redoc for the API documentation"}

@app.get("/symptoms", response_model=list[schemas.SymptomDefinitions])
async def list_symptoms(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymptomDefinitionsClient(db)
    return await client.list_symptoms(search_for)

@app.get("/symptoms/{symptom}", response_model=schemas.SymptomDefinitions)
async def get_symptom(symptom_name: str, db: AsyncSession = Depends(get_session)):
    client = SymptomDefinitionsClient(db)
    return await client.get_symptom(symptom_name)

@app.get("/diseaseGroups", response_model=list[schemas.DiseaseGroupDefinitions])
async def list_disease_groups(search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupDefinitionsClient(db)
    return await client.list_disease_groups(search_for)

@app.get("/diseaseGroups/{disease_group}", response_model=schemas.DiseaseGroupDefinitions)
async def get_disease_group(disease_group: str, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupDefinitionsClient(db)
    return await client.get_disease_group(disease_group)

@app.get('/bigTable', response_model=list[schemas.FullBigTable])
async def list_table_entries(db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.list_table_entries()

@app.get('/bigTable/{entry_id}', response_model=schemas.FullBigTable)
async def get_table_entry(table_entry_id: int, db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.get_table_entry(table_entry_id)

@app.post('/bigTable', response_model=schemas.FullBigTable)
async def post_table_entry(table_entry: schemas.BaseBigTable, dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    client = BigTableClient(db)
    return await client.add_entry(table_entry)

@app.get('/algorithmInput', response_model=None)
async def algorithm_input(db: AsyncSession = Depends(get_session)):
    client = SymptomsClient(db)
    return await client.create_algorithm_input()

@app.post('/evaluateAssessment', response_model=None)
async def evaluate_assessment(assessment: schemas.EvaluateAssessment, db: AsyncSession = Depends(get_session)):
    #TODO: Integrate with Halyna's code to evaluate the assessment
    if assessment:
        client = PredictionClient(db)
        received, predicted = await client.get_diagnose(assessment)
        return {"received": received, "predicted": predicted}

@app.post("/uploadfile", response_model=dict)
async def create_upload_file(
    file: UploadFile,
    dependencies=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session),
):
    print("Tutej 1")
    contents = await file.read()
    print("tutej", contents)
    buffer = BytesIO(contents)
    await read_xlsx_and_load_to_tables(buffer, db)
    df = pd.read_excel(buffer)
    buffer.close()

    #TODO: Integrate with Ahmed's code to save into a bigtable format
    #TODO: Save to DB

    return {"filename": file.filename, "columns": df.columns.to_list()}

@app.post("/login", response_model=schemas.TokenSchema)
async def login(user_credentials: schemas.UserModel, db: AsyncSession = Depends(get_session)):
    client = AuthClient(db)
    return await client.get_token(user_credentials)

#TODO: add response model
@app.get("/users")
async def list_users(dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    client = AuthClient(db)
    return await client.get_users()

@app.post("/change-password")
async def change_password(
    request: schemas.PasswordChange,
    dependencies=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session),
):
    client = AuthClient(db)
    return await client.change_pass(request)
    
"""
# TODO: fix issue in logout
@app.post("/logout")
async def logout(
    dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)
):
    client = AuthClient(db)
    token = dependencies
    payload = decodeJWT(token)
    user_id = str(payload["sub"])

    await client.remove_tokens(user_id=user_id)

    return {"message": "Logout Successfully"}
"""
