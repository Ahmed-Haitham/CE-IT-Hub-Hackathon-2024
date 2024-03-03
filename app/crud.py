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
        result.unique()
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
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY CASCADE")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class DiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_disease_group(self, entry_id: int):
        statement = select(models.DiseaseGroup).filter(models.DiseaseGroup.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()

    async def list_disease_groups(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.DiseaseGroup)
        if search_for:
            statement = statement.filter(
                models.DiseaseGroup.disease_group_medical_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        result.unique()
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.DiseaseGroup
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY CASCADE")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"  


class SymptomsDiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def populate_to_table(self, data):
        
        model = models.SymptomsDiseaseGroup
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"  

class SymmetricityClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_symmericity(self, entry_id: int):
        statement = select(models.Symmetricity).filter(models.Symmetricity.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_symmetricities(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.Symmetricity)
        if search_for:
            statement = statement.filter(
                models.Symmetricity.symmetricity_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.Symmetricity
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class ProgressionClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_progression(self, entry_id: int):
        statement = select(models.Progression).filter(models.Progression.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_progressions(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.Progression)
        if search_for:
            statement = statement.filter(
                models.Progression.symptom_medical_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.Progression
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class OnsetGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_onset_group(self, entry_id: int):
        statement = select(models.OnsetGroup).filter(models.OnsetGroup.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_onset_groups(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.OnsetGroup)
        if search_for:
            statement = statement.filter(
                models.OnsetGroup.onset_group_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.OnsetGroup
        table_instance = Base.metadata.tables[model.__tablename__]
        truncate_statement = text(f"TRUNCATE TABLE {table_instance} RESTART IDENTITY")
        await self.session.execute(truncate_statement)
        await self.session.commit()
        stmt = insert(model).values(data)
        await self.session.execute(stmt)
        await self.session.commit()
        return f"Table {table_instance} has been overwritten"


class TestCkLevelClient():
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_test_ck_level(self, entry_id: int):
        statement = select(models.TestCkLevel).filter(models.TestCkLevel.id == entry_id)
        result = await self.session.scalars(statement)
        return result.first()
        
    async def list_test_ck_levels(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.TestCkLevel)
        if search_for:
            statement = statement.filter(
                models.TestCkLevel.test_ck_level_name.ilike('%' + search_for + '%')
            )
        statement = statement.offset(skip).limit(limit)
        result = await self.session.scalars(statement)
        return result.all()
    
    async def populate_to_table(self, data):
        
        model = models.TestCkLevel
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
        self.session.add(new_entry)
        await self.session.commit()
        await self.session.refresh(new_entry)
        return new_entry