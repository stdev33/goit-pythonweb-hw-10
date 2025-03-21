from . import crud, models, schemas
from .auth import get_current_user
from .auth import router as auth_router
from .database import engine, get_db
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth_router)


@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please try again later."},
    )


@app.get("/me")
@limiter.limit("5/minute")
async def read_users_me(
    request: Request, current_user: schemas.UserResponse = Depends(get_current_user)
):
    return current_user


@app.post("/contacts/", response_model=schemas.ContactResponse, status_code=201)
def create_contact(
    contact: schemas.ContactCreate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    return crud.create_contact(db, contact)


@app.get("/contacts/", response_model=list[schemas.ContactResponse])
def get_contacts(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    return crud.get_contacts(db)


@app.get("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def get_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@app.put("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def update_contact(
    contact_id: int,
    contact: schemas.ContactUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    updated_contact = crud.update_contact(db, contact_id, contact)
    if not updated_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return updated_contact


@app.delete("/contacts/{contact_id}", response_model=schemas.ContactResponse)
def delete_contact(
    contact_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    deleted_contact = crud.delete_contact(db, contact_id)
    if not deleted_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return deleted_contact


@app.get("/search/")
def search_contacts(
    query: str,
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    return crud.search_contacts(db, query)


@app.get("/birthdays/")
def get_upcoming_birthdays(
    db: Session = Depends(get_db),
    current_user: schemas.UserResponse = Depends(get_current_user),
):
    return crud.get_upcoming_birthdays(db)
