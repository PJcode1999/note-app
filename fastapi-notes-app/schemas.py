import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional, List


# ---------- User Schemas ----------

class UserBase(BaseModel):
    user_name: str
    user_email: EmailStr


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    user_id: uuid.UUID
    create_on: datetime
    last_update: datetime

    class Config:
        from_attributes = True


# ---------- Auth Schemas ----------

class UserLogin(BaseModel):
    user_email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ---------- Note Schemas ----------

class NoteBase(BaseModel):
    note_title: str
    note_content: str


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    note_id: uuid.UUID
    created_on: datetime
    last_update: datetime

    class Config:
        from_attributes = True


# ---------- Response Schemas ----------

class UserWithNotes(UserRead):
    notes: List[NoteRead] = []
