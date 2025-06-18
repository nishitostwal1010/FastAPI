from pydantic import BaseModel, Field, computed_field, field_validator
from typing import Annotated, Literal
from config.city_tier import tier_1_cities, tier_2_cities

# Pydantic model to validate incomming data
class UserInput(BaseModel):

    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the user')]
    weight: Annotated[float, Field(..., gt=0, description='Weight of the user in kgs')]
    height: Annotated[float, Field(..., gt=0, lt=3, description='Height of the user in metres')]
    income_lpa: Annotated[float, Field(..., ge=0, description='Annula salary of the user in lpa')]
    smoker: Annotated[bool, Field(..., description='Is user a smoker?')]
    city: Annotated[str, Field(..., max_length=50, description='City of the user')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job', 'business_owner', 'unemployed', 'private_job'], Field(..., description='Occupation of the user')]

    @field_validator('city')
    @classmethod
    def normalize_city(cls, v: str) -> str:
        v = v.strip().title() # Frist char in capital rest in small case
        return v

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight / (self.height**2), 2)
    
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return 'young'
        elif self.age < 45:
            return 'adult'
        elif self.age < 60:
            return 'middle aged'
        return 'senior'

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return 'high'
        elif self.smoker or self.bmi > 27:
            return 'medium'
        else:
            return 'low'
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3