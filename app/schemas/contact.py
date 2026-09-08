from pydantic import BaseModel, EmailStr
from typing import Optional

class ContactSubmissionBase(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactSubmissionCreate(ContactSubmissionBase):
    pass

class ContactSubmissionResponse(ContactSubmissionBase):
    id: int
    status: str
    internal_notes: Optional[str] = None
    created_at: str
    updated_at: str
