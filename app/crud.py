from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi.encoders import jsonable_encoder

from . import models, schemas, auth


class SymptomClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom(self, symptom_name: str):
        statement = select(models.OneBigTable.symptom_medical_name, models.OneBigTable.symptom_description, models.OneBigTable.symptom_symmetricity, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_age_onset_group, models.OneBigTable.symptom_media_path, models.OneBigTable.symptom_tags).filter(models.OneBigTable.symptom_medical_name == symptom_name)
        #always require distinct for get single item endpoints
        statement = statement.distinct()
        result = await self.session.execute(statement)
        x = [row._mapping for row in result.all()]
        assert len(x)==1
        return x[0]
        
    async def list_symptoms(self, distinct_only, search_for, skip: int = 0, limit: int = 1000):
        statement = select(models.OneBigTable.symptom_medical_name, models.OneBigTable.symptom_description, models.OneBigTable.symptom_symmetricity, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_age_onset_group, models.OneBigTable.symptom_media_path, models.OneBigTable.symptom_tags)
        if distinct_only:
            statement = statement.distinct()
        if search_for:
            statement = statement.filter(
                #ilike is case insensitive like
                models.OneBigTable.symptom_medical_name.ilike('%' + search_for + '%') |
                #could not find a way to search for case insensitive tags in an array
                #could not find a way to seach for parts of a tag in an array
                models.OneBigTable.symptom_tags.contains([search_for]),
                )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)
        return [row._mapping for row in result.all()]

class DiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_disease_group(self, disease_group_name: str):
        statement = select(models.OneBigTable.disease_group_medical_name, models.OneBigTable.disease_group_summary_message, models.OneBigTable.test_ck_level).filter(models.OneBigTable.disease_group_medical_name == disease_group_name)
        statement = statement.distinct()
        result =  await self.session.execute(statement)
        x = [row._mapping for row in result.all()]
        assert len(x)==1
        return x[0]

    async def list_disease_groups(self, distinct_only, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.OneBigTable.disease_group_medical_name, models.OneBigTable.disease_group_summary_message, models.OneBigTable.test_ck_level)
        if distinct_only:
            statement = statement.distinct()
        if search_for:
            statement = statement.filter(
                models.OneBigTable.disease_group_medical_name.ilike('%' + search_for + '%')
                )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.execute(statement)
        x = [row._mapping for row in result.all()]
        return x

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
        self.session.add(new_entry)
        await self.session.commit()
        await self.session.refresh(new_entry)
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
        select(models.User).filter(models.User.username == change_pass_request.username)
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

    
