from pydantic import BaseModel, EmailStr, AnyUrl, Field, computed_field
from typing import Any, List, Dict, Optional, Annotated

# To compute BMI of patient using height and weight fields

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float #kgs
    height: float #meters
    married: bool
    allergies: Annotated[List[str], Field(default=None)]
    contact_details: Dict[str, str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi

def insert_patient_data(patient: Patient):

    print(patient.name)
    print(patient.weight)
    print(patient.height)
    print(patient.bmi)
    print('Data updated successfully')

patient_info = {'name':'Nishit', 'age': '80', 'weight': 67.2, 'height': 1.72, 'married': False, 'contact_details': {'phone': '9999999999', 'emergency': '9999999999'}, 'email': 'abc@hdfc.com'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
