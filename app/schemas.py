from pydantic import BaseModel, ConfigDict
from typing import List

from .models import SymmetricityChoices, ProgressionChoices, OnsetChoices, CkLevelChoices



class DiseaseSymptom(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    symptom_medical_name: str | None
    
class SymptomDisease(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None
    disease_group_medical_name: str | None

class BaseSymptoms(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_medical_name: str
    symptom_description: str | None
    symptom_media_path: str | None
    #TODO: can tags be null?
    symptom_tags: list[str] | None
    disease_group: List[SymptomDisease]

class FullSymptoms(BaseSymptoms):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disease_group_medical_name: str
    disease_group_summary: str | None
    associated_symptoms: List[DiseaseSymptom]

class FullDiseaseGroup(BaseDiseaseGroup):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseSymmetricity(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symmetricity_name: str

class FullSymmetricity(BaseSymmetricity):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseProgression(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    progression_name: str

class FullProgression(BaseProgression):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseOnsetGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    onset_group_name: str

class FullOnsetGroup(BaseOnsetGroup):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseTestCkLevel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    test_ck_level_name: str

class FullTestCkLevel(BaseTestCkLevel):
    model_config = ConfigDict(from_attributes=True)

    id: int

class BaseSymptomsDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_id: str | None
    disease_group_id: str | None

class FullBaseSymptomsDiseaseGroup(BaseSymptomsDiseaseGroup):
    model_config = ConfigDict(from_attributes=True)

    id: int

class SymptomBigTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_medical_name: str
    symptom_description: str | None
    #symptom_is_red_flag: bool
    #TODO: Enum validation should actually happen via pydantic models
    symptom_symmetricity: str
    symptom_progression: str
    symptom_age_onset_group: str
    symptom_media_path: str | None
    #TODO: can tags be null?
    symptom_tags: list[str] | None

class DiseaseGroupBigTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    disease_group_medical_name: str
    disease_group_summary_message: str
    test_ck_level: str

class BaseBigTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_medical_name: str
    symptom_description: str | None
    #symptom_is_red_flag: bool
    #TODO: Enum validation should actually happen via pydantic models
    symptom_symmetricity: str
    symptom_progression: str
    symptom_age_onset_group: str
    symptom_media_path: str | None
    #TODO: can tags be null?
    symptom_tags: list[str] | None
    disease_group_medical_name: str
    disease_group_summary_message: str
    test_ck_level: str

class FullBigTable(BaseBigTable):
    model_config = ConfigDict(from_attributes=True)

    id: int
    