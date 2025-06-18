from pydantic import BaseModel, Field
from typing import Dict

class PredictedResponse(BaseModel):

    predited_category: str = Field(..., description="The predicted insurance premium category", examples=["High","Medium","Low"])

    confidence: float = Field(..., description="Model's confidence score for the predicted class {range: 0 to 1}",)
    
    class_probabilites: dict[str, float] = Field(..., description="Probability distribution across all possible classes", examples=[{"Low":0.01, "Medium":0.30, "High":0.69}])