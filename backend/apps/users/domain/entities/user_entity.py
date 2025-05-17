from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime

@dataclass
class UserEntity:
    id: int
    username: str
    email: str
    password: Optional[str] = None
    
    name: Optional[str] = None
    surname: Optional[str] = None
    first_name: Optional[str] = None 
    last_name: Optional[str] = None  
    
    birth_date: Optional[datetime.date] = None 
    phone_number: Optional[str] = None
    
    is_active: bool = True
    is_staff: bool = False
    is_superuser: bool = False
    
    date_joined: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    
    email_verified: bool = False
    last_password_change: Optional[datetime] = None
    last_login_attempt: Optional[datetime] = None
