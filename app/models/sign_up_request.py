
from copy import deepcopy
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr

from app.models import User, Status



class SignUpRequest(BaseModel):
    email: EmailStr
    password: str
    username: str
    first_name: str
    last_name: str

    def deepcopy(self):
        return deepcopy(self)

    def to_user(self, user_id: UUID, status: Status, time_created: datetime, time_modified: datetime):
        return User(
            id=user_id,
            email=deepcopy(self.email),
            username=deepcopy(self.username),
            first_name=deepcopy(self.first_name),
            last_name=deepcopy(self.last_name),
            status=status,
            time_created=time_created,
            time_modified=time_modified
        )

