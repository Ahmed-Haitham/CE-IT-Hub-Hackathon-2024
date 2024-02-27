from .main import *


@app.post("/symptoms", response_model=schemas.Symptom)
def create_symptom(symptom: schemas.Symptom, db=Depends(get_db)):
    return crud.create_symptom(db, symptom)
