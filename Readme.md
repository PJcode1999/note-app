# Notes App API

A **FastAPI** application to manage personal notes with **JWT authentication**. Users can register, log in, and perform CRUD operations on their notes.

[GitHub Repository](https://github.com/PJcode1999/note-app.git)

---

## Table of Contents

* [Features](#features)
* [Tech Stack](#tech-stack)
* [Installation & Setup](#installation--setup)
* [Configuration](#configuration)
* [API Endpoints](#api-endpoints)
* [Authentication](#authentication)
* [Usage with Swagger UI](#usage-with-swagger-ui)
* [Usage with curl](#usage-with-curl)
* [Design Decisions & Trade-offs](#design-decisions--trade-offs)
* [External Resources](#external-resources)
* [License](#license)

---

## Features

* User registration and login
* JWT-based authentication
* CRUD operations for notes (Create, Read, Update, Delete)
* Fetch all notes or a single note by ID
* Validation, error handling, and timestamps for tracking

---

## Tech Stack

* **Backend:** Python, FastAPI
* **Database ORM:** SQLModel / SQLAlchemy
* **Database:** SQLite (default) / PostgreSQL (optional)
* **Authentication:** HTTPBearer / JWT
* **Server:** Uvicorn

---

## Installation & Setup

Clone the repository:

```bash
git clone https://github.com/PJcode1999/note-app.git
cd note-app
```

Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open in browser: `http://127.0.0.1:8000/docs` for Swagger UI.

---

## Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=sqlite:///./notes.db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> Optional: Use PostgreSQL by updating `DATABASE_URL`:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/notes_db
```

---

## API Endpoints

### 1. Register

**POST /register**

**Request:**

```json
{
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "password": "strongpassword"
}
```

**Response:**

```json
{
  "user_id": "uuid",
  "user_name": "John Doe",
  "user_email": "john@example.com",
  "create_on": "2025-09-20T14:00:00",
  "last_update": "2025-09-20T14:00:00"
}
```

---

### 2. Login

**POST /login**

**Request:**

```json
{
  "user_email": "john@example.com",
  "password": "strongpassword"
}
```

**Response:**

```json
{
  "access_token": "jwt_token_here",
  "token_type": "bearer"
}
```

---

### 3. Notes CRUD

All `/notes` endpoints require header:

```
Authorization: Bearer <token>
```

* **GET /notes** → Fetch all notes
* **POST /notes** → Create note
* **PUT /notes/{note\_id}** → Update note
* **DELETE /notes/{note\_id}** → Delete note

All endpoints return note data with UUID and timestamps.

---

### 4. Health Check

**GET /** → Public endpoint
**Response:** `{}`

---

## Authentication

* JWT-based authentication
* Include token in headers: `Authorization: Bearer <access_token>`
* Only authenticated users can access `/notes` endpoints

---

## Usage with Swagger UI

1. Run app: `uvicorn main:app --reload`
2. Open: `http://127.0.0.1:8000/docs`
3. Register → Login → Copy JWT token → Click **Authorize** → Access `/notes`

---

## Usage with curl

**Register:**

```bash
curl -X POST "http://127.0.0.1:8000/register" \
-H "Content-Type: application/json" \
-d '{"user_name":"John","user_email":"john@example.com","password":"pass123"}'
```

**Login:**

```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"user_email":"john@example.com","password":"pass123"}'
```

**Get Notes:**

```bash
curl -X GET "http://127.0.0.1:8000/notes" \
-H "Authorization: Bearer <access_token>"
```

**Create Note:**

```bash
curl -X POST "http://127.0.0.1:8000/notes" \
-H "Authorization: Bearer <access_token>" \
-H "Content-Type: application/json" \
-d '{"note_title":"Test Note","note_content":"Note content"}'
```

---

## Design Decisions & Trade-offs

1. **SQLite as default DB:** Simple, lightweight, no setup required for development. Optional PostgreSQL for production.
2. **JWT authentication:** Stateless, scalable, and secure.
3. **SQLModel / SQLAlchemy ORM:** Simplifies database operations, migrations, and relationships.
4. **UUIDs for IDs:** Ensures globally unique identifiers for users and notes.
5. **Error handling & validation:** Ensures API robustness and proper feedback.

**Trade-offs:**

* SQLite is not suitable for heavy concurrent usage; recommended PostgreSQL for production.
* JWT expiration handled via environment variable; token revocation requires additional logic if needed.

---

## External Resources

* [FastAPI Documentation](https://fastapi.tiangolo.com/) – Used as reference for building API structure.
* [SQLModel Documentation](https://sqlmodel.tiangolo.com/) – Simplified ORM design.
* [Passlib](https://passlib.readthedocs.io/) – Password hashing.
* [Python-JOSE](https://python-jose.readthedocs.io/) – JWT encoding/decoding.

> Note : All external code is referenced with official documentation links.

---