#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from . import models, schemas

async def _execute_statement(session: AsyncSession, statement):
    return await session.execute(statement)

class SymptomClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom(self, symptom_id: int):
        statement = select(models.Symptom).filter(models.Symptom.id == symptom_id)
        result =  await _execute_statement(self.session, statement)
        return result.scalar().all()

    async def list_symptoms(self, skip: int = 0, limit: int = 1000):
        statement = select(models.Symptom).offset(skip).limit(limit)
        result = await _execute_statement(self.session, statement)
        return result.scalars().all()

    async def create_symptom(self, symptom: schemas.CreateSymptom):
        new_symptom = models.Symptom(**symptom.model_dump())
        self.session.add(new_symptom)
        await self.session.commit()
        await self.session.refresh(new_symptom)
        return new_symptom

class DiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_disease_group(self, disease_group_id: int):
        statement = select(models.DiseaseGroup).filter(models.DiseaseGroup.id == disease_group_id)
        return await _execute_statement(self.session, statement)

    async def list_disease_groups(self, skip: int = 0, limit: int = 1000):
        statement = select(models.DiseaseGroup).offset(skip).limit(limit)
        return await _execute_statement(self.session, statement)

class AssocSymptomDiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom_disease_group_association(self, assoc_id: int):
        statement = select(models.AssocSymptomDiseaseGroup).filter(models.AssocSymptomDiseaseGroup.id == assoc_id)
        return await _execute_statement(self.session, statement)

    async def list_symptom_disease_group_associations(self, skip: int = 0, limit: int = 1000):
        statement = select(models.AssocSymptomDiseaseGroup).offset(skip).limit(limit)
        return await _execute_statement(self.session, statement)