#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException
from . import models, schemas
import logging

async def _execute_statement(session: AsyncSession, statement):
    return await session.scalars(statement)

class SymptomClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom(self, symptom_id: int):
        statement = select(models.Symptom).filter(models.Symptom.id == symptom_id)
        result =  await _execute_statement(self.session, statement)
        return result.first()

    async def list_symptoms(self, search_for, skip: int = 0, limit: int = 1000):
        statement = select(models.Symptom)
        if search_for:
            statement = statement.filter(
                #ilike is case insensitive like
                models.Symptom.medical_name.ilike('%' + search_for + '%') |
                #could not find a way to search for case insensitive tags in an array
                #could not find a way to seach for parts of a tag in an array
                models.Symptom.tags.contains([search_for]),
                )
        statement = statement.offset(skip).limit(limit)
        result = await _execute_statement(self.session, statement)
        return result.all()

    async def create_symptom(self, symptom: schemas.CreateSymptom):
        new_symptom = models.Symptom(**symptom.model_dump())
        self.session.add(new_symptom)
        #Using flush here, and commit in the caller function did not work
        await self.session.commit()
        await self.session.refresh(new_symptom)
        return new_symptom

class DiseaseGroupClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_disease_group(self, disease_group_id: int, return_relationships: bool):
        if return_relationships:
            logging.info("returning relationships")
            statement = select(models.DiseaseGroup, models.Symptom).filter(
                models.DiseaseGroup.id == disease_group_id).options(
                    joinedload(models.DiseaseGroup.has_symptoms), 
                    joinedload(models.DiseaseGroup.has_required_symptoms),
                    joinedload(models.DiseaseGroup.has_excluding_symptoms)
                )
        else:
            statement = select(models.DiseaseGroup).filter(models.DiseaseGroup.id == disease_group_id)
        result =  await _execute_statement(self.session, statement)
        return result.first()

    async def list_disease_groups(self, search_for: str, skip: int = 0, limit: int = 1000):
        statement = select(models.DiseaseGroup)
        if search_for:
            statement = statement.filter(
                models.DiseaseGroup.medical_name.ilike('%' + search_for + '%')
                )
        statement = statement.offset(skip).limit(limit)
        result = await _execute_statement(self.session, statement)
        return result.all()

    async def create_disease_group(self, disease_group: schemas.CreateDiseaseGroup, links: schemas.CreateLinksSubmission | None = None):
        new_disease_group = models.DiseaseGroup(**disease_group.model_dump())
        if links:
            #There are some relationships to add. Need to get a proper schema from db
            async def symptom_lookup_id(symptom):
                '''Search for id or name of a symptom in the db'''
                if type(symptom) == str:
                    #name was passed
                    read_symptom = await symptom_client.list_symptoms(search_for=symptom)
                    try:
                        assert len(read_symptom) == 1
                    except AssertionError:
                        if len(read_symptom) > 1:
                            raise HTTPException(status_code=500, detail=f"More than one matching symptom found: {symptom}")
                        else:
                            raise HTTPException(status_code=404, detail=f"Cannot add relationship to symptom not found in db: {symptom}")
                    result = read_symptom[0].id
                else:
                    #id was passed, validate that it's in the db
                    result = await symptom_client.get_symptom(symptom)
                return result
            symptom_client = SymptomClient(self.session)
            if links.symptoms_list:
                related_symptoms = []
                for symptom in links.symptoms_list:
                    related_symptoms.append(await symptom_lookup_id(symptom))
                new_disease_group.has_symptoms = related_symptoms
            if links.required_symptoms_list:
                required_symptoms = []
                for symptom in links.required_symptoms_list:
                    required_symptoms.append(await symptom_lookup_id(symptom))
                new_disease_group.required_symptoms = required_symptoms
            if links.excluding_symptoms_list:
                excluding_symptoms = []
                for symptom in links.excluding_symptoms_list:
                    excluding_symptoms.append(await symptom_lookup_id(symptom))
                new_disease_group.excluding_symptoms = excluding_symptoms
        self.session.add(new_disease_group)
        await self.session.commit()
        await self.session.refresh(new_disease_group)
        return new_disease_group