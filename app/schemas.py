from pydantic import BaseModel, ConfigDict
from typing import Optional

class BaseSymptom(BaseModel):
    #https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)

    medical_name: str
    description: Optional[str]
    symmetricity: Optional[str]
    progression: Optional[str]
    age_onset_group: Optional[str]
    media_path: Optional[str]
    tags: list[str]

class CreateSymptom(BaseSymptom):
    is_red_flag: Optional[bool]

class ReadSymptom(BaseSymptom):
    id: int
    is_red_flag: bool

class BaseDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medical_name: str
    summary_message: Optional[str]

class CreateDiseaseGroup(BaseDiseaseGroup):
    pass

class ReadDiseaseGroup(BaseDiseaseGroup):
    id: int

class AssocSymptomDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symptom_id: int
    disease_group_id: int