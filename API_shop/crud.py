""" CRUD methods"""

from fastapi import APIRouter
from schemas.shopping import CartItem

router = APIRouter(tags=["Shopping Cart"])

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

@router.delete("/delete-item-cart/{cart_id}")
def delete_cart_item(cart_id: int):
    """ Deletes item from shopping cart"""

    valid = len(shopping_cart) > cart_id
    if valid:
        item = shopping_cart[cart_id]
        shopping_cart.pop(cart_id)

    response = {"response": f"item with id {item} was removed from cart"}
    return response 


@router.put("/update-item-cart/{cart_id}")
def update_cart_item(cart_id: int, cart_item: CartItem):
    """ Updates item in shopping cart"""

    valid = len(shopping_cart) > cart_id
    if valid:
        item = shopping_cart[cart_id]
        shopping_cart[cart_id] = cart_item.item

    response = {"response": f"item {item} with id {cart_id} was updated to {cart_item.item}"}
    return response
