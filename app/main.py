# app/main.py

from datetime import datetime
from io import BytesIO

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
# TODO: move sqlalchemy related code to crud/models
from sqlalchemy import String, cast, delete, select
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.auth import (
    JWTBearer,
    decodeJWT,
)
from app.crud import BigTableClient, DiseaseGroupClient, SymptomClient, AuthClient, PredictionClient
from app.db import engine, get_session, start_db

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

@app.get("/")
async def root():
    return {"message": "See /docs or /redoc for the API documentation"}

@app.get("/symptoms", response_model=list[schemas.SymptomBigTable])
async def list_symptoms(distinct_only: bool = True, search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.list_symptoms(distinct_only, search_for)

@app.get("/symptoms/{symptom}", response_model=schemas.SymptomBigTable)
async def get_symptom(symptom_name: str, db: AsyncSession = Depends(get_session)):
    client = SymptomClient(db)
    return await client.get_symptom(symptom_name)

@app.get("/diseaseGroups", response_model=list[schemas.DiseaseGroupBigTable])
async def list_disease_groups(distinct_only: bool = True, search_for: str | None = None, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
    return await client.list_disease_groups(distinct_only, search_for)

@app.get("/diseaseGroups/{disease_group}", response_model=schemas.DiseaseGroupBigTable)
async def get_disease_group(disease_group: str, db: AsyncSession = Depends(get_session)):
    client = DiseaseGroupClient(db)
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

@app.post('/evaluateAssessment', response_model=None)
async def evaluate_assessment(assessment: schemas.EvaluateAssessment, db: AsyncSession = Depends(get_session)):
    #TODO: Integrate with Halyna's code to evaluate the assessment
    if assessment:
        client = PredictionClient(db)
        predicted = await client.get_diagnose(assessment)
        return {"received": assessment, "predicted": predicted}

@app.post("/uploadfile/", response_model=dict)
def create_upload_file(file: UploadFile, dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_excel(buffer)
    buffer.close()
    file.file.close()
    #TODO: Integrate with Ahmed's code to save into a bigtable format
    #TODO: Save to DB

    return {"filename": file.filename, "columns": df.columns.to_list()}

#TODO: remove this endpoint once live, as anyone can hit it to get a JWT key now with admin privileges
@app.post("/register", response_model=dict[str, str])
async def register_user(user: schemas.UserModel, db: AsyncSession = Depends(get_session)):
    client = AuthClient(db)
    return await client.add_user(user)


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
    
'''
# TODO: fix issue in logout
@app.post("/logout")
async def logout(
    dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)
):
    token = dependencies
    payload = decodeJWT(token)
    user_id = payload["sub"]

    await db.execute(
        delete(models.TokenTable).where(
            cast(models.TokenTable.user_id, String) == str(user_id),
        )
    )
    await db.commit()

    return {"message": "Logout Successfully"}
'''