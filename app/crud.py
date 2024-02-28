#from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from sqlalchemy.orm.mapper import Mapper
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
    async def get_disease_group(self, disease_group_id: int):
        statement = select(models.DiseaseGroup).filter(models.DiseaseGroup.id == disease_group_id)
        result =  await _execute_statement(self.session, statement)
        return result.first()

    async def list_disease_groups(self, search_for, skip: int = 0, limit: int = 1000):
        statement = select(models.DiseaseGroup)
        if search_for:
            statement = statement.filter(
                models.DiseaseGroup.medical_name.ilike('%' + search_for + '%')
                )
        statement = statement.offset(skip).limit(limit)
        result = await _execute_statement(self.session, statement)
        return result.all()

    async def create_disease_group(self, disease_group: schemas.CreateDiseaseGroup):
        new_disease_group = models.DiseaseGroup(**disease_group.model_dump())
        self.session.add(new_disease_group)
        await self.session.commit()
        await self.session.refresh(new_disease_group)
        return new_disease_group

    #This isn't a method of the linkingclient below because it needs to be called after the disease group is created
    #and I could not pass the sessions from one client to another.
    async def create_symptom_disease_group_link(self, associations: list[dict]):
        symptom_client = SymptomClient(self.session)
        async def symptom_lookup_id(symptom):
            '''Search for id or name of a symptom in the db'''
            if type(symptom) == str:
                #name was passed
                read_symptom = await symptom_client.list_symptoms(search_for=symptom)
            else:
                #id was passed, validate that it's in the db
                read_symptom = await symptom_client.get_symptom(symptom)
            #Need to make sure the returned symptom list is of length 1
            try:
                assert len(read_symptom) == 1
            except AssertionError:
                if len(read_symptom) > 1:
                    raise HTTPException(status_code=500, detail=f"More than one matching symptom found: {symptom}")
                else:
                    raise HTTPException(status_code=404, detail=f"Cannot add relationship to symptom not found in db: {symptom}")
            return read_symptom[0].id
        
        for i in range(len(associations)):
            #add the symptom id to the dictionary from the db
            symptom_id = await symptom_lookup_id(associations[i]['symptom'])
            associations[i].update({'symptom_id': symptom_id})
            associations[i].pop("symptom")
            logging.info(f"Sending dict to link table: {associations[i]}")
            link_insert = models.link_symptom_disease_group.insert().values(
                **associations[i])
            await self.session.execute(link_insert)
            self.session.commit()
        #TODO: This isn't working, not sure why, but the links are not being added anyway
        #link_client = LinkingClient(self.session)
        #return await link_client.list_symptom_disease_group_links(associations[0]['disease_group_id'])
        return []

class LinkingClient():
    def __init__(self, session: AsyncSession):
        self.session = session
    async def get_symptom_disease_group_link(self, symptom_id: int, disease_group_id: int):
        statement = select(models.link_symptom_disease_group).filter(
            models.link_symptom_disease_group.disease_group_id == disease_group_id,
            models.link_symptom_disease_group.symptom_id == symptom_id
            )
        result =  await _execute_statement(self.session, statement)
        return result.first()

    async def list_symptom_disease_group_links(self, disease_group_id: int = None, skip: int = 0, limit: int = 1000):
        statement = select(models.link_symptom_disease_group)
        if disease_group_id:
            statement = statement.filter(
                models.link_symptom_disease_group.disease_group_id == disease_group_id
                )
        statement = statement.offset(skip).limit(limit)
        result =  await _execute_statement(self.session, statement)
        return result.all()