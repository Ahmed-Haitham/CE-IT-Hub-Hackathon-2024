# app/main.py

from datetime import datetime
from io import BytesIO

import pandas as pd
from fastapi import Depends, FastAPI, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import String, cast, delete, select
from fastapi.middleware.cors import CORSMiddleware

# TODO: move sqlalchemy related code to crud/models
from sqlalchemy.ext.asyncio import AsyncSession

from app import models, schemas
from app.auth import (
    JWTBearer,
    create_access_token,
    create_refresh_token,
    decodeJWT,
    get_hashed_password,
    token_required,
    verify_password,
)
from app.crud import BigTableClient, DiseaseGroupClient, SymptomClient
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

@app.get('/bigTable', response_model=list[schemas.FullBigTable])# here there is an issue with the schema of the response 
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
    if assessment:
        return {"received": assessment}

@app.post("/uploadfile/", response_model=dict)
@token_required
def create_upload_file(file: UploadFile, dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)):
    contents = file.file.read()
    buffer = BytesIO(contents)
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

@app.post("/register")
async def register_user(
    user: schemas.UserCreate, db: AsyncSession = Depends(get_session)
):
    existing_user = await db.execute(
        select(models.User).filter_by(username=user.username)
    )

    if existing_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = models.User(username=user.username, password=encrypted_password)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "user created successfully"}


@app.post("/login", response_model=schemas.TokenSchema)
async def login(
    request: schemas.requestdetails, db: AsyncSession = Depends(get_session)
):
    user = await db.scalar(
        select(models.User).filter(models.User.username == request.username)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
        )

    if not verify_password(request.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
        )

    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    token_db = models.TokenTable(
        user_id=user.id, access_token=access, refresh_token=refresh, status=True
    )
    db.add(token_db)
    await db.commit()
    await db.refresh(token_db)
    return {
        "access_token": access,
        "refresh_token": refresh,
    }


@app.get("/getusers")
@token_required
async def getusers(
    dependencies=Depends(JWTBearer()), db: AsyncSession = Depends(get_session)
):
    result = await db.execute(select(models.User))
    return [jsonable_encoder(user) for user in result.scalars()]


@app.post("/change-password")
@token_required
async def change_password(
    request: schemas.changepassword,
    dependencies=Depends(JWTBearer()),
    db: AsyncSession = Depends(get_session),
):
    user = await db.scalar(
        select(models.User).filter(models.User.username == request.username)
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )

    if not verify_password(request.old_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password"
        )

    encrypted_password = get_hashed_password(request.new_password)
    user.password = encrypted_password
    await db.commit()

    return {"message": "Password changed successfully"}

# TODO: fix issue in logout
@app.post("/logout")
@token_required
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
