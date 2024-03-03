from pydantic import BaseModel, ConfigDict

from .models import SymmetricityChoices, ProgressionChoices, OnsetChoices, CkLevelChoices



class BaseSymptoms(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_medical_name: str
    symptom_description: str

class FullSymptoms(BaseSymptoms):
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
    