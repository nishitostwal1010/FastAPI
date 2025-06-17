from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
import json

app = FastAPI()


class Patient(BaseModel):

    id: Annotated[str, Field(...,  description='Id of patient', examples=['P001'])]
    name: Annotated[str, Field(..., max_length=50, description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in meters')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'


class PatientUpdate(BaseModel):

    name: Annotated[Optional[str], Field(max_length=50, description='Name of the patient', default=None)]
    city: Annotated[Optional[str], Field(description='City where the patient is living', default=None)]
    age: Annotated[Optional[int], Field(gt=0, lt=120, description='Age of the patient', default=None)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(description='Gender of the patient', default=None)]
    height: Annotated[Optional[float], Field(gt=0, description='Height of the patient in meters', default=None)]
    weight: Annotated[Optional[float], Field(gt=0, description='Weight of the patient in kgs', default=None)]


def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)

    return data


def save_data(data):
    with open('patients.json', mode='w') as f:
        json.dump(data, f)


@app.get('/')
def hello():
    return {'message':'Patient Management System API'}


@app.get('/about')
def about():
    return {'key':'A fully functional API to manage patient records'}


@app.get('/view')
def view():
    data = load_data()

    return data


@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description='ID of patient in the DB', example='P001')):
    # load all the patients
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not found')


@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight or bmi'), order_by: str = Query('asc', description='Sort in asc or desc order')):

    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order_by not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order, select between asc and desc')
    
    data = load_data()

    sort_order = True if order_by=='desc' else False

    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order)

    return sorted_data


@app.post('/create')
def create_patient(patient: Patient):

    # load existing data
    data = load_data()

    # check if patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail='Patient already exist')

    # new patient added to the database
    data[patient.id] = patient.model_dump(exclude=['id'])

    # save into the json file
    save_data(data)

    return JSONResponse(status_code=201, content={'message':'Patient created successfully'})


@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    
    # load exisiting data
    data = load_data()

    # check if patient exists or not 
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient does not exist')
    
    existing_patient_info = data[patient_id]

    new_patient_info = patient_update.model_dump(exclude_unset=True) # Exclude all the fields which are null(not given)

    for key, value in new_patient_info.items():
        existing_patient_info[key] = value

    # As BMI is calculated field so if weight is updated we need to update BMI as well.
    # The reason we didn't give BMI as well in Pydantic model is that weight can be None if no new weight is given.

    # To solve this we will create a new Patient model object so that we get all computed_fields as well with new values.

    # Steps -> existing_patient_info -> Pydantic object -> Got calculated fields(BMI, verdict) -> Conver to Dict -> Store 
    existing_patient_info['id'] = patient_id
    patient_pydantic_object = Patient(**existing_patient_info)

    patient_dict = patient_pydantic_object.model_dump(exclude=['id'])

    data[patient_id] = patient_dict

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient updated'})


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient not found')

    del data[patient_id]

    save_data(data)

    return JSONResponse(status_code=200, content={'message': 'Patient deleted'})
