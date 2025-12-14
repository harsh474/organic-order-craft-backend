from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from .order_item import OrderItem

class Item(SQLModel, table=True):
    __tablename__ = "items"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int
    volume: int

    order_items: List["OrderItem"] = Relationship(back_populates="item")
