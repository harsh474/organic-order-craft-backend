from typing import Optional,TYPE_CHECKING
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship 

if TYPE_CHECKING : 
    from .order import Order 

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, nullable=False, unique=True)
    hashed_password: str
    phone: str = Field(nullable=False)
    address: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    orders : list["Order"] = Relationship(back_populates="users") 
    