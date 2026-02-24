""" CRUD methods"""

from fastapi import APIRouter
from schemas.shopping import CartItem

router = APIRouter()

shopping_cart = []

@router.get("/shopping-cart")
def query_shopping_cart():
    """ Returns shopping cart"""
    response = {"response": shopping_cart}
    return response

@router.get("/shopping-cart/{cart_id}")
def query_shopping_cart(cart_id: int):
    """ Returns shopping cart"""

    response = {"response": f"item with id {cart_id} does not exist"}
    valid = len(shopping_cart) > cart_id

    if valid:
        response = {"response": shopping_cart[cart_id]}

    return response


@router.post("/add-to-cart")
def add_to_cart(cart_item: CartItem):
    """ Adds item to shopping cart"""

    shopping_cart.append(cart_item.item)
    response = {"response": f"Item added to cart: {cart_item.item} added"}
    return response 
