import datetime

from pydantic import BaseModel, ConfigDict

from .models import (
    CkLevelChoices,
    OnsetChoices,
    ProgressionChoices,
    SymmetricityChoices,
)


class UserModel(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class PasswordChange(BaseModel):
    username: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime


class SymptomBigTable(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    symptom_medical_name: str
    symptom_description: str | None
    # symptom_is_red_flag: bool
    # TODO: Enum validation should actually happen via pydantic models
    symptom_symmetricity: str
    symptom_progression: str
    symptom_age_onset_group: str
    symptom_media_path: str | None
    # TODO: can tags be null?
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
    # symptom_is_red_flag: bool
    # TODO: Enum validation should actually happen via pydantic models
    symptom_symmetricity: str
    symptom_progression: str
    symptom_age_onset_group: str
    symptom_media_path: str | None
    # TODO: can tags be null?
    symptom_tags: list[str] | None
    disease_group_medical_name: str
    disease_group_summary_message: str
    test_ck_level: str

class FullBigTable(BaseBigTable):
    model_config = ConfigDict(from_attributes=True)

    id: int
    
class EvaluateAssessment(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    selectedActor: str
    selectedSymptoms: list[str]
    selectedProgression: list[str]
    selectedSymmetricity: list[str]
    selectedFamilyHistory: list[bool]
    selectedCk: str
    selectedAgeOnset: str