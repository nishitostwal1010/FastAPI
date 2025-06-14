from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Annotated, Required, Optional

class Patient(BaseModel):

    name: Annotated[str, Field(max_length=50, title='Name of the patient', description='Give the name of the patient in less than 50 char', examples=['Nishit', 'Ostwal'], default='Nishit')]
    age: int = Field(gt=0, lt=120, default=18)
    weight: Annotated[float, Field(gt=0, strict=True)]
    married: bool
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]
    email: EmailStr
    url: AnyUrl
  
def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_details)
    print(patient.email)
    print(patient.url)
    print('Inserted into database')

patient_info = {'name':'Nishit', 'age': 30, 'weight': 67.2, 'married': False, 'contact_details': {'phone': '9999999999'}, 'email': 'abc@gmail.com', 'url': 'https://abc.com'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
