from sqlalchemy.orm import Session

from . import models, schemas

#Get and list functions to read from the DB
def get_symptom(db: Session, symptom_id: int):
    return db.query(models.Symptom).filter(models.Symptom.id == symptom_id).one_or_none()

def list_symptoms(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.Symptom).offset(skip).limit(limit).all()

def get_disease_group(db: Session, disease_group_id: int):
    return db.query(models.DiseaseGroup).filter(models.DiseaseGroup.id == disease_group_id).one_or_none()

def list_disease_groups(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.DiseaseGroup).offset(skip).limit(limit).all()

def get_symptom_disease_group_association(db: Session, assoc_id: int):
    return db.query(models.AssocSymptomDiseaseGroup).filter(models.AssocSymptomDiseaseGroup.id == assoc_id).one_or_none()

def list_symptom_disease_group_associations(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.AssocSymptomDiseaseGroup).offset(skip).limit(limit).all()

#Create functions to write to the DB
def create_symptom(db: Session, symptom: schemas.Symptom):
    db_symptom = models.Symptom(**symptom.model_dump())
    db.add(db_symptom)
    db.commit()
    db.refresh(db_symptom)
    return db_symptom