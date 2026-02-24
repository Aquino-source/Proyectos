"""Schemas for shopping cart"""

from pydantic import BaseModel

class CartItem(BaseModel):
    """ Cart item schema """
    item:str
