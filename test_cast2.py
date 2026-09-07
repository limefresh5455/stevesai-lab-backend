from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional, Union, Any

class FlexibleIn(BaseModel):
    model_config = ConfigDict(extra='allow')

class FlexibleOut(FlexibleIn):
    id: Union[str, int]
    created_at: Optional[str] = None

class CaseStudyOut(FlexibleOut):
    project_year: Optional[str] = None
    
    @field_validator('project_year', mode='before')
    def cast_to_str(cls, v):
        if v is not None:
            return str(v)
        return v

obj = CaseStudyOut(id=1, project_year=2023, other_field="hello")
print(obj.model_dump())
