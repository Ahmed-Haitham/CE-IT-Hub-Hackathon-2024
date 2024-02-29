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

class BaseDiseaseGroup(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    medical_name: str
    summary_message: str

class CreateSymptom(BaseSymptom):
    pass

class CreateDiseaseGroup(BaseDiseaseGroup):
    pass

class ReadSymptom(BaseSymptom):
    id: int

class ReadDiseaseGroup(BaseDiseaseGroup):
    id: int

class ReadRelatedSymptom(ReadSymptom):
    appears_in_diseases: list[ReadDiseaseGroup] | None = None
    required_in_diseases: list[ReadDiseaseGroup] | None = None
    excluding_in_diseases: list[ReadDiseaseGroup] | None = None

class ReadRelatedDiseaseGroup(ReadDiseaseGroup):
    has_symptoms: list[ReadSymptom] | None = None
    has_required_symptoms: list[ReadSymptom] | None = None
    has_excluding_symptoms: list[ReadSymptom] | None = None

class CreateLinksSubmission(BaseModel):
    symptoms_list: list[int] | list[str] | None = None
    required_symptoms_list: list[int] | list[str] | None = None
    excluding_symptoms_list: list[int] | list[str] | None = None
