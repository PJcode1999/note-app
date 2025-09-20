import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    user_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    user_name: str
    user_email: str = Field(index=True, unique=True)
    password: str
    last_update: datetime = Field(default_factory=datetime.utcnow)
    create_on: datetime = Field(default_factory=datetime.utcnow)

    notes: List["Note"] = Relationship(back_populates="owner")


class Note(SQLModel, table=True):
    note_id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    note_title: str
    note_content: str
    last_update: datetime = Field(default_factory=datetime.utcnow)
    created_on: datetime = Field(default_factory=datetime.utcnow)

    owner_id: uuid.UUID = Field(foreign_key="user.user_id")
    owner: Optional[User] = Relationship(back_populates="notes")
