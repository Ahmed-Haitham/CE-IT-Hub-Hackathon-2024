import enum
from typing import List
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Enum, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship, Mapped
from .db import Base

class SymmetricityChoices(enum.Enum):
    '''bilateral = "Bilateral: Both sides of the body are affected"
    unilateral = "Unilateral: Only one side of the body is affected"
    na = "Not Applicable"
    '''
    unilateral = "asymetryczny"
    bilateral = "symetryczny"
    na = "na"

class ProgressionChoices(enum.Enum):
    '''
    variable = "Variable: Periods of deterioration and improvement"
    persistent = "Persistent: Symptoms are always present with constant intensity"
    slow_progressing = "Slowly progressing: Symptoms slowly worsen over years"
    medium_progressing = "Medium progressing: Symptoms gradually worsen over months"
    fast_progressing = "Fast progressing: Symptoms rapidly worsen over days or weeks"\
    '''
    stable = "stałe/postępujące"
    variable = "zmienne"

class OnsetChoices(enum.Enum):
    '''
    congenital = "Congenital: Present at birth"
    childhood = "Childhood: Appeared before 10 years old"
    adolescence = "Adolescence: Appeared between 10 and 20 years old"
    young_adulthood = "Young adulthood: Appeared between 20 and 30 years old"
    middle_age = "Middle age: Appeared between 30 and 50 years old"
    senior = "Senior: Appeared after 50 years old"
    '''
    birth = "od urodzenia / wczesnego niemowlęctwa"
    under_ten = "<10 rż"
    ten_to_twenty = "10-20rż"
    twenty_to_thirty = "20-30rż"
    thirty_to_fifty = "30-50  rż"
    over_fifty = ">50rż"

class CkLevelChoices(enum.Enum):
    normal = "norma"
    over_one_k = "powyżej normy do 1000"
    one_k_to_ten_k = ">1000 do 10000"
    over_ten_k = "> 10000"
    not_tested = "nie było oznaczone (komunikat- wykonaj badanie)"

class OneBigTable(Base):
    __tablename__ = "big_table"

    id = Column(Integer, default=None, primary_key=True)
    symptom_medical_name = Column(String(128), nullable=False)
    symptom_description = Column(String(5000))
    #symptom_is_red_flag = Column(Boolean, default=False)
    symptom_symmetricity = Column(Enum(SymmetricityChoices), default="na", nullable=False)
    symptom_progression = Column(Enum(ProgressionChoices), nullable=False)
    symptom_age_onset_group = Column(Enum(OnsetChoices), nullable=False)
    symptom_media_path = Column(String(128))
    symptom_tags = Column(ARRAY(String), nullable=False)

    disease_group_medical_name = Column(String(128), nullable=False)#, unique=True
    disease_group_summary_message = Column(String(5000), nullable=False)

    test_ck_level = Column(Enum(CkLevelChoices), default="not_tested")

class Symptoms(Base):
    __tablename__ = "symptom"

    id = Column(Integer, default=None, primary_key=True)
    symptom_medical_name = Column(String(999), nullable=False, unique=True)
    symptom_description = Column(String(5000))
    symptom_media_path = Column(String(128))
    symptom_tags = Column(ARRAY(String), nullable=True) # After development phase it shuld be nullable=False
    disease_group = relationship('DiseaseGroup', back_populates="associated_symptoms", secondary="symptoms_disease_group", lazy="joined")
    excluding_in_diseases = relationship('DiseaseGroup', back_populates="excluding_symptoms", secondary="ex_symptoms_disease_group", lazy="joined")


class DiseaseGroup(Base):
    __tablename__ = "disease_group"

    id = Column(Integer, default=None, primary_key=True)
    disease_group_medical_name = Column(String(999), nullable=False, unique=True)
    disease_group_summary = Column(String(5000))
    associated_symptoms = relationship('Symptoms', back_populates="disease_group", secondary="symptoms_disease_group", lazy="joined")
    excluding_symptoms = relationship('Symptoms', back_populates="excluding_in_diseases", secondary="ex_symptoms_disease_group", lazy="joined")

class SymptomsDiseaseGroup(Base):
    __tablename__ = "symptoms_disease_group"

    id = Column(Integer, default=None, primary_key=True)
    symptom_id = Column(String(999), ForeignKey("symptom.symptom_medical_name"))
    disease_group_id = Column(String(999), ForeignKey("disease_group.disease_group_medical_name"))


class ExSymptomsDiseaseGroup(Base):
    __tablename__ = "ex_symptoms_disease_group"

    id = Column(Integer, default=None, primary_key=True)
    symptom_id = Column(String(999), ForeignKey("symptom.symptom_medical_name"))
    disease_group_id = Column(String(999), ForeignKey("disease_group.disease_group_medical_name"))


class Symmetricity(Base):
    __tablename__ = "symmetricity"

    id = Column(Integer, default=None, primary_key=True)
    symmetricity_name = Column(String(999), nullable=False)


class Progression(Base):
    __tablename__ = "progression"

    id = Column(Integer, default=None, primary_key=True)
    progression_name = Column(String(999), nullable=False)


class OnsetGroup(Base):
    __tablename__ = "onset_group"

    id = Column(Integer, default=None, primary_key=True)
    onset_group_name = Column(String(999), nullable=False)


class TestCkLevel(Base):
    __tablename__ = "test_ck_level"

    id = Column(Integer, default=None, primary_key=True)
    test_ck_level_name = Column(String(999), nullable=False)