from sqlmodel import SQLModel, Field,Relationship
from typing import Optional ,TYPE_CHECKING
from datetime import datetime 


if TYPE_CHECKING : 
     from .user import User 
     from .item import Item
     from .OrderItem import OrderItem


class Order(SQLModel,table= True): 
     __tablename__ = "orders" 
     id : Optional[int]  = Field(default=None, primary_key=True) 
     order_date : datetime  = Field(default_factory=datetime.utcnow)
     delivered_address:str 
     
     order_items: list["OrderItem"] = Relationship(back_populates ="order")
     
     user_id: int = Field(default =None,foreign_key="users.id") 
     user : Optional["User"]  =Relationship(back_populates="orders")
     
     
