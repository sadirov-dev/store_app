from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from store_app.api.dependencies import get_current_user
from store_app.database.db import get_db
from store_app.database.schemas import CartAdd, CartItemResponse, CartUpdate
from store_app.services.cart_service import add_to_cart, clear_cart, delete_cart_item, get_user_cart, update_cart_item


router = APIRouter(prefix="/api/cart", tags=["Cart"])


@router.post("/add", response_model=CartItemResponse, status_code=201)
def add_to_cart_view(
    cart_data: CartAdd,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return add_to_cart(db, current_user, cart_data)


@router.get("", response_model=list[CartItemResponse])
def get_cart_view(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_cart(db, current_user)


@router.patch("/{item_id}", response_model=CartItemResponse)
def update_cart_item_view(
    item_id: int,
    cart_data: CartUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_cart_item(db, current_user, item_id, cart_data)


@router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
def clear_cart_view(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    clear_cart(db, current_user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cart_item_view(item_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    delete_cart_item(db, current_user, item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
