from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator
from typing import List, Dict, Optional, Annotated

# Using field_validator to do custom validation on a field, transform data present in a field

class Patient(BaseModel):

    name: str
    email: EmailStr
    age: int
    weight: float
    married: bool
    allergies: Annotated[List[str], Field(default=None)]
    contact_details: Dict[str, str]

    # To check if email is of hdfc or icici or not
    @field_validator('email')
    @classmethod
    def email_validator(cls, value): # In cls we get the class which contains the validator(so we can access class constants, methods but not other fields) and value contains the value of the specified field (In this case value of email field)

        valid_domains = ['hdfc.com', 'icici.com']

        #abc@gmail.com -> we want to extract gmail.com from it
        domain_name = value.split('@')[-1]

        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        
        return value
    
    # To transform name to uppercase
    @field_validator('name')
    @classmethod
    def transform_name(cls, value):
        return value.upper()
    
    # To check if age is 0-100 before/after type coercion, therefore if I give mode='before' in field_validator then error will ve shown as age is given as '30' and validator will say that comparision between integer and string is not possible ( 0 < '30' < 100)
    @field_validator('age')
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError('Age should be between 0 and 100')

def insert_patient_data(patient: Patient):

    print(patient.name)
    print('Data updated successfully')

patient_info = {'name':'Nishit', 'age': '30', 'weight': 67.2, 'married': False, 'contact_details': {'phone': '9999999999'}, 'email': 'abc@hdfc.com'}

patient1 = Patient(**patient_info)

insert_patient_data(patient1)
