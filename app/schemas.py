from pydantic import BaseModel, ConfigDict
from typing import Optional

class Symptom(BaseModel):
    #https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)

    id: int
    medical_name: str
    description: Optional[str]
    is_red_flag: bool
    symmetricity: Optional[str]
    progression: Optional[str]
    age_onset_group: Optional[str]
    media_path: Optional[str]
    tags: list[str]

class DiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    medical_name: str
    summary_message: Optional[str]
    excluding_symptoms: Optional[list[int]]
    required_symptoms: Optional[list[int]]

class AssocSymptomDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    symptom_id: int
    disease_group_id: int