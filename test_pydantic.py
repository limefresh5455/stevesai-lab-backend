from app.schemas.content import FlexibleIn
obj = FlexibleIn(**{"title": "new title"})
print(obj.model_dump(exclude_unset=True))
print(obj.model_dump())
