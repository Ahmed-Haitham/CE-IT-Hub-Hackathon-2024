import datetime
import enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.dialects.postgresql import ARRAY

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(100), nullable=False)


class TokenTable(Base):
    __tablename__ = "token"
    user_id = Column(Integer)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)


class SymmetricityChoices(enum.Enum):
    """bilateral = "Bilateral: Both sides of the body are affected"
    unilateral = "Unilateral: Only one side of the body is affected"
    na = "Not Applicable"
    """

    unilateral = "asymetryczny"
    bilateral = "symetryczny"
    na = "na"


class ProgressionChoices(enum.Enum):
    """
    variable = "Variable: Periods of deterioration and improvement"
    persistent = "Persistent: Symptoms are always present with constant intensity"
    slow_progressing = "Slowly progressing: Symptoms slowly worsen over years"
    medium_progressing = "Medium progressing: Symptoms gradually worsen over months"
    fast_progressing = "Fast progressing: Symptoms rapidly worsen over days or weeks"\
    """

    stable = "stałe/postępujące"
    variable = "zmienne"
    progressing = "postępujące"


class OnsetChoices(enum.Enum):
    """
    congenital = "Congenital: Present at birth"
    childhood = "Childhood: Appeared before 10 years old"
    adolescence = "Adolescence: Appeared between 10 and 20 years old"
    young_adulthood = "Young adulthood: Appeared between 20 and 30 years old"
    middle_age = "Middle age: Appeared between 30 and 50 years old"
    senior = "Senior: Appeared after 50 years old"
    """

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

class GenderChoices(enum.Enum):
    female = "płeć żeńska"
    male = "płeć męska"

class OneBigTable(Base):
    __tablename__ = "big_table"

    id = Column(Integer, default=None, primary_key=True)
    symptom_medical_name = Column(String(128), nullable=False)
    symptom_description = Column(String(5000))
    # symptom_is_red_flag = Column(Boolean, default=False)
    symptom_symmetricity = Column(
        Enum(SymmetricityChoices), default="na", nullable=False
    )
    symptom_progression = Column(Enum(ProgressionChoices), nullable=False)
    first_symptom_age_onset_group = Column(Enum(OnsetChoices), nullable=False)
    symptom_media_path = Column(String(128))
    symptom_tags = Column(ARRAY(String), nullable=False)

    disease_group_medical_name = Column(String(128), nullable=False)  # , unique=True
    disease_group_summary_message = Column(String(5000), nullable=False)

    test_ck_level = Column(Enum(CkLevelChoices), default="not_tested")

    gender = Column(Enum(GenderChoices), nullable=False)


class SymptomDefinitions(Base):
    __tablename__ = "symptoms_definition"

    id = Column(Integer, default=None, primary_key=True)
    symptom_medical_name = Column(String(999), nullable=False, unique=True)
    symptom_description = Column(String(999))
    symptom_media_path = Column(String(128))
    symptom_tags = Column(ARRAY(String))


class DiseaseGroupDefinitions(Base):
    __tablename__ = "disease_groups_definition"

    id = Column(Integer, default=None, primary_key=True)
    disease_group_medical_name = Column(String(999), nullable=False, unique=True)


class SymptomsValidation(Base):
    __tablename__ = "symptoms_validation"

    id = Column(Integer, default=None, primary_key=True)
    pseudo_symptom_name = Column(String(3000), nullable=False, unique=True)

class Symptoms(Base):
    __tablename__ = "symptoms"

    id = Column(Integer, default=None, primary_key=True)
    symptom_name = Column(String(3000)) #TODO set back foreign key constraint, ForeignKey("symptoms_validation.pseudo_symptom_name"), nullable=False)
    symptom_category = Column(String(128))
    disease_name = Column(String(128))
    disease_code = Column(String(128))
