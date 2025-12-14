from sqlmodel import Field ,Relationship,SQLModel
from typing import Optional  ,TYPE_CHECKING


if TYPE_CHECKING : 
     from .item import Item
     from .order import Order 
     
class OrderItem(SQLModel,table = True):  
     __tablename__ = "order_items"

     id: Optional[int] = Field(default=None, primary_key=True)

     order_id: int = Field(foreign_key="orders.id")
     item_id: int = Field(foreign_key="items.id")

     quantity: int
     
     order: Optional["Order"] = Relationship(back_populates="order_items")
     item: Optional["Item"] = Relationship(back_populates="order_items")
     
     
     