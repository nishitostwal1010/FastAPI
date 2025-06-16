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

print(patient1)
print(patient1.name)
print(patient1.address.city)
print(patient1.address.pin)