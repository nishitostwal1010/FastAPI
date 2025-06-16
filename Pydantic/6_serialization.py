from pydantic import BaseModel

# The Patient pydantic model can have address which can also be a pydantic model

class Address(BaseModel):

    city: str
    state: str
    pin: str

class Patient(BaseModel):

    name: str
    gender: str
    age: int
    address: Address

address_dict = {'city': 'gurgaon', 'state': 'haryana', 'pin': '122001'}

address1 = Address(**address_dict)

patient_dict = {'name': 'Nishit', 'gender': 'male', 'age': '22', 'address': address1}

patient1 = Patient(**patient_dict)

patient1_dict = patient1.model_dump(include=['name','age','address']) # Converts Pydantic object to Python dictionary

print(patient1_dict)
print(type(patient1_dict))

patient1_json = patient1.model_dump_json(exclude={'address':['city','state']})

print(patient1_json)
print(type(patient1_json))