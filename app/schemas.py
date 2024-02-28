from pydantic import BaseModel, ConfigDict

from .models import SymmetricityChoices, ProgressionChoices, OnsetChoices

#https://fastapi.tiangolo.com/tutorial/body/#request-body
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
    #accept ids or symptom names, or lists of them

class CreateDiseaseGroup(BaseDiseaseGroup):
    pass

class ReadDiseaseGroup(BaseDiseaseGroup):
    id: int

class CreateLinksSubmission(BaseModel):
    '''Accepts both ids and names for symptoms'''
    symptoms_list: list[str] | list[int] | None = None
    required_symptoms_list: list[str] | list[int] | None = None
    excluding_symptoms_list: list[str] | list[int] | None = None

class CreateLinks(CreateLinksSubmission):
    disease_group_id: int

class ReadSymptomDiseaseGroupLink(BaseModel):
    disease_group_id: int
    symptom_id: int