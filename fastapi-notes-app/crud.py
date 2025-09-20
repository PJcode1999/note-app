from sqlmodel import Session, select
from typing import List, Optional
from models import User, Note
from auth import get_password_hash
from uuid import UUID


# ---------- User CRUD ----------

def create_user(session: Session, user_name: str, user_email: str, password: str) -> User:
    hashed_password = get_password_hash(password)
    user = User(user_name=user_name, user_email=user_email, password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.user_email == email)
    return session.exec(statement).first()


def get_user(session: Session, user_id: str) -> Optional[User]:
    statement = select(User).where(User.user_id == user_id)
    return session.exec(statement).first()


def get_all_users(session: Session) -> List[User]:
    statement = select(User)
    return session.exec(statement).all()


# ---------- Notes CRUD ----------

def create_note(session: Session, owner_id: str, note_title: str, note_content: str) -> Note:
    note = Note(owner_id=owner_id, note_title=note_title, note_content=note_content)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def get_note(session: Session, note_id: str) -> Optional[Note]:
    note_uuid = UUID(note_id)
    statement = select(Note).where(Note.note_id == note_uuid)
    return session.exec(statement).first()


def get_notes_by_user(session: Session, owner_id: str) -> List[Note]:
    statement = select(Note).where(Note.owner_id == owner_id)
    return session.exec(statement).all()


def update_note(session: Session, note_id: str, note_title: str, note_content: str) -> Optional[Note]:
    note = get_note(session, note_id)
    if note:
        note.note_title = note_title
        note.note_content = note_content
        session.add(note)
        session.commit()
        session.refresh(note)
    return note


def delete_note(session: Session, note_id: str) -> bool:
    note = get_note(session, note_id)
    if note:
        session.delete(note)
        session.commit()
        return True
    return False
