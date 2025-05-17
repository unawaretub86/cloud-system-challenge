from dataclasses import dataclass, field
from typing import Optional
import uuid

@dataclass
class User:
    username: str
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True
    is_staff: bool = False
    id: uuid.UUID = field(default_factory=uuid.uuid4)
