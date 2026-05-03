from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ── Register ──────────────────────────────────────────────
class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=128)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class RegisterResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# ── Login ─────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ── Refresh ───────────────────────────────────────────────
class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
