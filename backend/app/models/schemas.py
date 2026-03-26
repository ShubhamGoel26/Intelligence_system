from pydantic import BaseModel
from typing import Optional

class BusinessProfile(BaseModel):
    name: str
    location: Optional[str]
    description: Optional[str]
    size_signals: Optional[str]
    digital_presence: Optional[str]
    tools_used: Optional[str]

class ContactCard(BaseModel):
    phone: Optional[str]
    email: Optional[str]
    whatsapp: Optional[str]
    source: Optional[str]

class LeadResult(BaseModel):
    company: str
    profile: BusinessProfile
    contact: ContactCard
    outreach_message: str