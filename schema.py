from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Command Schemas ---
class CommandRequest(BaseModel):
    command: str

class CommandResponse(BaseModel):
    status: str          # "EXECUTED" or "REJECTED"
    message: str         # "Command ran successfully" or "Blocked by rule..."
    credits_remaining: int

# --- Rule Schemas (For Admins) ---
class RuleCreate(BaseModel):
    pattern: str
    action: str  # "allow" or "block"
    description: Optional[str] = None

class RuleResponse(RuleCreate):
    id: int
    class Config:
        from_attributes = True

# --- User Schema ---
class UserProfile(BaseModel):
    username: str
    role: str
    credits: int

# --- Audit Log Schema ---
# ... existing imports ...

class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    username: str   # <--- NEW FIELD
    command: str
    status: str
    response: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True