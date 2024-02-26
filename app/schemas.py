from pydantic import BaseModel, ConfigDict
from typing import Optional

from .models import SymmetricityChoices, ProgressionChoices, OnsetChoices

class BaseSymptom(BaseModel):
    #https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)

    medical_name: str
    description: str | None = None
    is_red_flag: bool | None = False
    symmetricity: str | None = 'na'
    progression: str
    age_onset_group: str
    media_path: str | None = None
    tags: list[str]

class CreateSymptom(BaseSymptom):
    pass

class ReadSymptom(BaseSymptom):
    id: int

class BaseDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medical_name: str
    summary_message: str

class CreateDiseaseGroup(BaseDiseaseGroup):
    pass

class ReadDiseaseGroup(BaseDiseaseGroup):
    id: int

class AssocSymptomDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symptom_id: int
    disease_group_id: int