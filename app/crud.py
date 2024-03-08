from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, text, delete, cast, String
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import DBAPIError

from . import models, schemas, auth
from .db import Base
from .prepare_dataset import convert_long_to_dictionary
import pandas as pd

class SymptomDefinitionsClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_symptom(self, entry_id: int):
        statement = select(models.SymptomDefinitions).filter(models.SymptomDefinitions.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_symptoms(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.SymptomDefinitions)
        if search_for:
            statement = statement.filter(
                models.SymptomDefinitions.symptom_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        result.unique()
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.SymptomDefinitions
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"
    

class DiseaseGroupDefinitionsClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_disease_group(self, entry_id: int):
        statement = select(models.DiseaseGroupDefinitions).filter(models.DiseaseGroupDefinitions.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()

    async def list_disease_groups(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.DiseaseGroupDefinitions)
        if search_for:
            statement = statement.filter(
                models.DiseaseGroupDefinitions.disease_group_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        result.unique()
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.DiseaseGroupDefinitions
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class SymptomsValidationClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def populate_to_table(self, data):
     
        model = models.SymptomsValidation
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY CASCADE")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class SymptomsClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_algorithm_input(self):
        statement = select(Base.metadata.tables[models.Symptoms.__tablename__])
        result = await self.session.execute(statement)
        return convert_long_to_dictionary(result.mappings().all())


    async def populate_to_table(self, data):
      
        model = models.Symptoms
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"
 

class BigTableClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_table_entry(self, entry_id: int):
        statement = select(models.OneBigTable).filter(models.OneBigTable.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()

    async def list_table_entries(self, skip: int = 0, limit: int = 1000):
        statement = select(models.OneBigTable)
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()

    async def add_entry(self, entry: schemas.BaseBigTable):
        new_entry = models.OneBigTable(**entry.model_dump())
        try:
            self.session.add(new_entry)
            await self.session.commit()
            await self.session.refresh(new_entry)
        except DBAPIError as e:
            if 'invalid input value' in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid enum value received: " + str(e.orig)
                )
        return new_entry

class AuthClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_token(self, user_credentials: schemas.UserModel):
        user = await self.session.scalar(
            select(models.User).filter(models.User.username == user_credentials.username)
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username"
            )
        if not auth.verify_password(user_credentials.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password"
            )
        access = auth.create_access_token(user.id)
        refresh = auth.create_refresh_token(user.id)
        token_db = models.TokenTable(
            user_id=user.id, access_token=access, refresh_token=refresh, status=True
        )
        self.session.add(token_db)
        await self.session.commit()
        await self.session.refresh(token_db)
        return {
            "access_token": access,
            "refresh_token": refresh,
        }

    async def add_user(self, user):
        existing_user = await self.session.execute(
            select(models.User).filter_by(username=user.username)
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Username already registered")
        encrypted_password = auth.get_hashed_password(user.password)
        new_user = models.User(username=user.username, password=encrypted_password)
        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)
        return {"message": "user created successfully"}

    async def get_users(self):
        result = await self.session.execute(select(models.User))
        return [jsonable_encoder(user) for user in result.scalars()]

    async def change_pass(self, change_pass_request):
        user = await self.session.scalar(
            select(models.User).filter(
                models.User.username == change_pass_request.username
            )
        )
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
            )
        if not auth.verify_password(change_pass_request.old_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid old password"
            )
        encrypted_password = auth.get_hashed_password(change_pass_request.new_password)
        user.password = encrypted_password
        await self.session.commit()
        return {"message": "Password changed successfully"}

    async def remove_tokens(self, user_id: str):
        await self.session.execute(
            delete(models.TokenTable).where(
                cast(models.TokenTable.user_id, String) == user_id,
            )
        )
        await self.session.commit()


class PredictionClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    def _parse_user_input(self, user_input):
        user_input = user_input.dict()
        listlike_keys = {key: user_input[key] for key in ['selectedSymptoms', 'selectedProgression', 'selectedSymmetricity', 'selectedFamilyHistory']}
        df = pd.DataFrame(listlike_keys)
        df["selectedCk"] = user_input["selectedCk"]
        df['selectedAgeOnset'] = user_input['selectedAgeOnset']
        df['gender'] = 'male' if user_input['female_gender'][0] == False else 'female'
        df['family_member'] = None
        df['comorbosities'] = None
        df.columns = [
            'symptom_medical_name',
            'symptom_progression',
            'symptom_symmetricity',
            'symptom_in_family_history',
            'test_ck_level',
            'first_symptom_age_onset_group',
            'gender',
            'family_member',
            'comorbosities'
        ]
        return df

    async def get_diagnose(self, evaluation_request: schemas.EvaluateAssessment):
        user_inputs_df = self._parse_user_input(evaluation_request)
        print(user_inputs_df.to_dict(orient='records'))
        #TODO: Use real algorithm to predict
        predicted = [
            {
                "disease": "Parkinson's Disease",
                "probability": 0.8,
            },
            {
                "disease": "Multiple Sclerosis",
                "probability": 0.1,
            },
            {
                "disease": "Alzheimer's Disease",
                "probability": 0.05,
            },
            {
                "disease": "Huntington's Disease",
                "probability": 0.05,
            }
        ]
        return [user_inputs_df.to_dict(orient='records'), predicted]