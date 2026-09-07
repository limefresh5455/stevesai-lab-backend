from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Any, List, Optional, Dict, Union

class FlexibleIn(BaseModel):
    model_config = ConfigDict(extra='allow')

class FlexibleOut(FlexibleIn):
    id: Union[str, int]
    created_at: Optional[Any] = None

class BlogOut(FlexibleOut): pass
class BlogCreate(FlexibleIn): pass
class BlogUpdate(FlexibleIn): pass

class ServiceOut(FlexibleOut): pass
class ServiceCreate(FlexibleIn): pass
class ServiceUpdate(FlexibleIn): pass

class CaseStudyOut(FlexibleOut):
    project_year: Optional[str] = None
    
    @field_validator('project_year', mode='before')
    @classmethod
    def cast_project_year_to_str(cls, v):
        if v is not None:
            return str(v)
        return v
class CaseStudyCreate(FlexibleIn): pass
class CaseStudyUpdate(FlexibleIn): pass

class PageOut(FlexibleOut): pass
class PageCreate(FlexibleIn): pass
class PageUpdate(FlexibleIn): pass
