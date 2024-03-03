from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, distinct, text
from fastapi import HTTPException
from . import models, schemas
from .db import Base

class SymptomClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom(self, entry_id: int):
        statement = select(models.Symptoms).filter(models.Symptoms.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_symptoms(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.Symptoms)
        if search_for:
            statement = statement.filter(
                models.Symptoms.symptom_medical_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()
    
    async def add_symptom(self, entry: schemas.BaseSymptoms):
        new_entry = models.Symptoms(**entry.model_dump())
        self.session.add(new_entry)
        await self.session.commit()
        await self.session.refresh(new_entry)
        return new_entry
    
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