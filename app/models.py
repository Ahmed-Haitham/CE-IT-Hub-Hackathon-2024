import enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, DeclarativeBase
from .db import Base

class SymmetricityChoices(enum.Enum):
    bilateral = "Bilateral: Both sides of the body are affected"
    unilateral = "Unilateral: Only one side of the body is affected"
    na = "Not Applicable"

class ProgressionChoices(enum.Enum):
    variable = "Variable: Periods of deterioration and improvement"
    persistent = "Persistent: Symptoms are always present with constant intensity"
    slow_progressing = "Slowly progressing: Symptoms slowly worsen over years"
    medium_progressing = "Medium progressing: Symptoms gradually worsen over months"
    fast_progressing = "Fast progressing: Symptoms rapidly worsen over days or weeks"

class OnsetChoices(enum.Enum):
    congenital = "Congenital: Present at birth"
    childhood = "Childhood: Appeared before 10 years old"
    adolescence = "Adolescence: Appeared between 10 and 20 years old"
    young_adulthood = "Young adulthood: Appeared between 20 and 30 years old"
    middle_age = "Middle age: Appeared between 30 and 50 years old"
    senior = "Senior: Appeared after 50 years old"

#https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
link_symptom_disease_group = Table(
    'link_symptom_disease_group',
    Base.metadata,
    Column('symptom_id', ForeignKey('symptoms.id'), primary_key=True),
    Column('disease_group_id', ForeignKey('disease_groups.id'), primary_key=True)
    )

required_symptoms = Table(
    'required_symptoms',
    Base.metadata,
    Column('disease_group_id', ForeignKey('disease_groups.id'), primary_key=True),
    Column('required_symptom_id', ForeignKey('symptoms.id'), primary_key=True)
    )

excluding_symptoms = Table(
    'excluding_symptoms',
    Base.metadata,
    Column('disease_group_id', ForeignKey('disease_groups.id'), primary_key=True),
    Column('excluding_symptom_id', ForeignKey('symptoms.id'), primary_key=True)
    )

class Symptom(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, default=None, primary_key=True)
    medical_name = Column(String(128), nullable=False)
    description = Column(String(5000))
    is_red_flag = Column(Boolean, default=False)
    symmetricity = Column(Enum(SymmetricityChoices), default="na")
    progression = Column(Enum(ProgressionChoices), nullable=False)
    age_onset_group = Column(Enum(OnsetChoices), nullable=False)
    media_path = Column(String(128))
    tags = Column(ARRAY(String), nullable=False)

    appears_in_diseases = relationship("DiseaseGroup", secondary=link_symptom_disease_group, back_populates="has_symptoms")
    required_in_diseases = relationship("DiseaseGroup", secondary=required_symptoms, back_populates="has_required_symptoms")
    excluding_in_diseases = relationship("DiseaseGroup", secondary=excluding_symptoms, back_populates="has_excluding_symptoms")

class DiseaseGroup(Base):
    __tablename__ = "disease_groups"

    id = Column(Integer, default=None, primary_key=True)
    medical_name = Column(String(128), nullable=False)
    summary_message = Column(String(5000), nullable=False)

    has_symptoms = relationship("Symptom", secondary=link_symptom_disease_group, back_populates="appears_in_diseases")
    has_required_symptoms = relationship("Symptom", secondary=required_symptoms, back_populates="required_in_diseases")
    has_excluding_symptoms = relationship("Symptom", secondary=excluding_symptoms, back_populates="excluding_in_diseases")