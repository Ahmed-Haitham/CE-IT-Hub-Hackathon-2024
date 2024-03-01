from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from . import models, schemas

class SymptomClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom(self, symptom_name: str):
        statement = select(models.OneBigTable.symptom_medical_name, models.OneBigTable.symptom_description, models.OneBigTable.symptom_symmetricity, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_age_onset_group, models.OneBigTable.symptom_media_path, models.OneBigTable.symptom_tags).filter(models.OneBigTable.symptom_medical_name == symptom_name)
        result = await self.session.execute(statement)
        x = [row._mapping for row in result.all()]
        assert len(x)==1
        return x[0]
        
    async def list_symptoms(self, search_for, skip: int = 0, limit: int = 1000):
        statement = select(models.OneBigTable.symptom_medical_name, models.OneBigTable.symptom_description, models.OneBigTable.symptom_symmetricity, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_progression, models.OneBigTable.symptom_age_onset_group, models.OneBigTable.symptom_media_path, models.OneBigTable.symptom_tags)
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
        result =  await self.session.execute(statement)
        x = [row._mapping for row in result.all()]
        assert len(x)==1
        return x[0]

    async def list_disease_groups(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.OneBigTable.disease_group_medical_name, models.OneBigTable.disease_group_summary_message, models.OneBigTable.test_ck_level)
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
