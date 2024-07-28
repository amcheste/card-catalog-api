from enum import Enum
from pydantic import BaseModel


class Status(str, Enum):
    active = 'ACTIVE'
    disabled = 'DISABLED'
