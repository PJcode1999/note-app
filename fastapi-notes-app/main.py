from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from database import init_db, get_session
from models import User, Note
from schemas import UserCreate, UserRead, UserLogin, Token, NoteCreate, NoteRead
from auth import authenticate_user, create_access_token, get_current_user
import crud

# Initialize DB tables
init_db()

app = FastAPI(title="Notes App")

# ------------------- User Routes -------------------

@app.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user with JSON payload."""
    existing_user = crud.get_user_by_email(session, user.user_email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = crud.create_user(session, user.user_name, user.user_email, user.password)
    return new_user

@app.post("/login", response_model=Token)
def login(user: UserLogin, session: Session = Depends(get_session)):
    """Login using JSON payload, returns JWT token."""
    authenticated_user = authenticate_user(session, user.user_email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token({"sub": authenticated_user.user_email})
    return {"access_token": access_token, "token_type": "bearer"}

# ------------------- Notes Routes (JWT Protected) -------------------

@app.post("/notes", response_model=NoteRead)
def create_note(
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a note for the logged-in user."""
    return crud.create_note(session, current_user.user_id, note.note_title, note.note_content)

@app.get("/notes", response_model=List[NoteRead])
def get_notes(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all notes for the logged-in user."""
    return crud.get_notes_by_user(session, current_user.user_id)

@app.put("/notes/{note_id}", response_model=NoteRead)
def read_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    note = crud.get_note(session, note_id) 

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    return note 


@app.put("/notes/{note_id}", response_model=NoteRead)
def update_note(
    note_id: str,
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Update a note owned by the logged-in user."""
    existing_note = crud.get_note(session, note_id)
    if not existing_note or str(existing_note.owner_id) != str(current_user.user_id):
        raise HTTPException(status_code=404, detail="Note not found")
    return crud.update_note(session, note_id, note.note_title, note.note_content)

@app.delete("/notes/{note_id}", status_code=204)
def delete_note(
    note_id: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Delete a note owned by the logged-in user."""
    existing_note = crud.get_note(session, note_id)
    if not existing_note or str(existing_note.owner_id) != str(current_user.user_id):
        raise HTTPException(status_code=404, detail="Note not found")
    crud.delete_note(session, note_id)
    return {"message": 'Node deleted!'}

# ------------------- Health Check -------------------

@app.get("/")
def health():
    """Public health check."""
    return {"status": "ok"}
