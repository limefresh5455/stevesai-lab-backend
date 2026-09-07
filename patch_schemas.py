import re

with open("app/schemas/content.py", "r") as f:
    content = f.read()

# Add field_validator to import
if "field_validator" not in content:
    content = content.replace("from pydantic import BaseModel, ConfigDict", "from pydantic import BaseModel, ConfigDict, field_validator")

# Replace CaseStudyOut
old_case = "class CaseStudyOut(FlexibleOut): pass"
new_case = """class CaseStudyOut(FlexibleOut):
    project_year: Optional[str] = None
    
    @field_validator('project_year', mode='before')
    @classmethod
    def cast_project_year_to_str(cls, v):
        if v is not None:
            return str(v)
        return v"""

content = content.replace(old_case, new_case)

with open("app/schemas/content.py", "w") as f:
    f.write(content)
