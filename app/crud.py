from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, text, delete, cast, String
from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.exc import DBAPIError

from . import models, schemas, auth
from .db import Base
from .prepare_dataset import convert_long_to_dictionary
from .prediction_algorithm import predict_disease_excl, parse_disease
from .models import CkLevelChoices, ProgressionChoices, SymmetricityChoices, OnsetChoices
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
        symmetricity_dict = {key: member.value for key, member in SymmetricityChoices.__members__.items()}
        progression_dict = {key: member.value for key, member in ProgressionChoices.__members__.items()}
        onset_dict = {key: member.value for key, member in OnsetChoices.__members__.items()}
        ck_level_dict = {key: member.value for key, member in CkLevelChoices.__members__.items()}
        user_input = user_input.dict()
        
        translated_input = myinput.copy()
        # Translate selectedSymmetricity
        translated_input["selectedSymmetricity"] = [symmetricity_dict.get(value, value) for value in translated_input["selectedSymmetricity"]]
        # Translate selectedProgression
        translated_input["selectedProgression"] = [progression_dict.get(value, value) for value in translated_input["selectedProgression"]]
        # Translate selectedAgeOnset
        translated_input["selectedAgeOnset"] = onset_dict.get(translated_input["selectedAgeOnset"], translated_input["selectedAgeOnset"])
        # Translate selectedCk
        translated_input["selectedCk"] = ck_level_dict.get(translated_input["selectedCk"], translated_input["selectedCk"])
        # Translate selectedGender
        if translated_input.get("female_gender"):
            translated_input["female_gender"] = [GenderChoices.female.value if value else GenderChoices.male.value for value in translated_input["female_gender"]]
        # Translate selectedSymptoms
        translated_input["selectedSymptoms"] = [symptom for symptom in translated_input["selectedSymptoms"]]

        translation_dict = {'selectedActor': 'wybranyAktor',
                'selectedSymptoms': 'nazwa objawu',
                'selectedProgression': 'nasilenie w czasie',
                'selectedSymmetricity': 'cechy objawu',
                'selectedFamilyHistory': 'wywiad',
                'selectedCk': 'poziom ck',
                'selectedAgeOnset': 'wiek wystapienia pierwszych objawów',
                'female_gender': 'plec'}
        desired_keys = ['grupa objawów',
                        'nazwa objawu',
                        'nasilenie w czasie',
                        'dynamika objawów',
                        'cechy objawu',
                        'wiek wystapienia pierwszych objawów',
                        'wywiad rodzinny - czy w rodzinie są lub były osoby z podobnymi objawami jak u pacjenta. jeśli tak to proszę wybrac pokrewiensto',
                        'wywiad rodzinny - czy w rodzinie do 2 pokoleń wstecz występowały poniższe objawy',
                        'grupa chorób',
                        'poziom ck',
                        'objawy obligatoryjne',
                        'objawy wykluczające',
                        'choroby współistniejące',
                        'podgrupa chorób',
                        'cechy charakterystyczne i objawy współistniejące',
                        'jednostka chorobowa']
        desired_input = {translation_dict.get(k, k): v for k, v in translated_input.items()}
        for key in desired_input:
            if isinstance(desired_input[key], list):
                desired_input[key] = [desired_input[key][0]]
            else:
                desired_input[key] = [desired_input[key]]

        desired_input = {k: desired_input[k] for k in desired_keys if k in desired_input}
        return desired_input
    
    async def create_algorithm_input(self):
        statement = select(Base.metadata.tables[models.Symptoms.__tablename__])
        result = await self.session.execute(statement)
        return convert_long_to_dictionary(result.mappings().all())

    async def get_diagnose(self, evaluation_request: schemas.EvaluateAssessment):
        user_inputs_df = self._parse_user_input(evaluation_request)
        # print(user_inputs_df.to_dict(orient='records'))
        algorithm_input =  await self.create_algorithm_input()
        predicted = parse_disease(predict_disease_excl(user_inputs_df, algorithm_input))

        #TODO: Use real algorithm to predict
        # predicted = [
        #     {
        #         "disease": "Parkinson's Disease",
        #         "probability": 0.8,
        #         "symptoms": ["jittering", "trouble speaking"],
        #         "mandatory_symptoms": ["jittering"],
        #         "excluding_symptoms": ["ptosis"]
        #     },
        #     {
        #         "disease": "Multiple Sclerosis",
        #         "probability": 0.1,
        #         "symptoms": ["numbness", "trouble walking"],
        #         "mandatory_symptoms": ["numbness"],
        #         "excluding_symptoms": []
        #     },
        #     {
        #         "disease": "Alzheimer's Disease",
        #         "probability": 0.05,
        #         "symptoms": ["memory loss", "trouble concentrating"],
        #         "mandatory_symptoms": [],
        #         "excluding_symptoms": []
        #     },
        #     {
        #         "disease": "Huntington's Disease",
        #         "probability": 0.05,
        #         "symptoms": ["involuntary movements", "trouble walking"],
        #         "mandatory_symptoms": [],
        #         "excluding_symptoms": ["ck_over_1000"]
        #     }
        # ]
        return [user_inputs_df.to_dict(orient='records'), predicted]