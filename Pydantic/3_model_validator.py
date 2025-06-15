from pydantic import BaseModel, EmailStr, AnyUrl, Field, model_validator
from typing import List, Dict, Optional, Annotated

# To check if patient age is 60 or not. If yes then check if a field - 'emergency no.' is present or not.
# If not then don't add the Patient details

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Annotated[List[str], Field(default=None)]
    contact_details: Dict[str, str]

    @model_validator(mode='after')
    @classmethod
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact_details:
            raise ValueError('Patients older than 60 must have an emergency contact')
        return model


def insert_patient_data(patient: Patient):

    print(patient.name)
    print('Data updated successfully')

patient_info = {'name':'Nishit', 'age': '80', 'weight': 67.2, 'married': False, 'contact_details': {'phone': '9999999999', 'emergency': '9999999999'}, 'email': 'abc@hdfc.com'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
