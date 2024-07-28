from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr
from app.models.status import Status


class User(BaseModel):
    """
    User
    """
    id: UUID          # User uuid
    email: EmailStr       # User's email
    username: str    # Username
    first_name: str  # User's first name
    last_name: str    # User's last name
    status: Status
    time_created: datetime
    time_modified: datetime


class UserRequest(BaseModel):
    email: EmailStr       # User's email
    username: str    # Username
    first_name: str  # User's first name
    last_name: str    # User's last name
