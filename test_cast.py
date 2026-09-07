from pydantic import BaseModel, ConfigDict
from typing import Optional, Union

class FlexibleIn(BaseModel):
    model_config = ConfigDict(extra='allow')

class FlexibleOut(FlexibleIn):
    id: Union[str, int]
    created_at: Optional[str] = None

class CaseStudyOut(FlexibleOut):
    project_year: Optional[str] = None

obj = CaseStudyOut(id=1, project_year=2023, other_field="hello")
print(obj.model_dump())
