from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from store_app.database import models, schemas
from store_app.services.product_service import get_product_by_id


def add_to_cart(db: Session, user: models.User, cart_data: schemas.CartAdd) -> models.CartItem:
    product = get_product_by_id(db, cart_data.product_id)
    if product.quantity < cart_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough product quantity in stock")

    cart_item = (
        db.query(models.CartItem)
        .filter(
            models.CartItem.user_id == user.id,
            models.CartItem.product_id == cart_data.product_id,
        )
        .first()
    )

    if cart_item:
        new_quantity = cart_item.quantity + cart_data.quantity
        if product.quantity < new_quantity:
            raise HTTPException(status_code=400, detail="Not enough product quantity in stock")
        cart_item.quantity = new_quantity
    else:
        cart_item = models.CartItem(
            user_id=user.id,
            product_id=cart_data.product_id,
            quantity=cart_data.quantity,
        )
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item


def get_user_cart(db: Session, user: models.User) -> list[models.CartItem]:
    return (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.user_id == user.id)
        .order_by(models.CartItem.id.desc())
        .all()
    )


def get_cart_item_by_id(db: Session, user: models.User, item_id: int) -> models.CartItem:
    cart_item = (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.id == item_id, models.CartItem.user_id == user.id)
        .first()
    )
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return cart_item


def update_cart_item(db: Session, user: models.User, item_id: int, cart_data: schemas.CartUpdate) -> models.CartItem:
    cart_item = get_cart_item_by_id(db, user, item_id)
    product = get_product_by_id(db, cart_item.product_id)

    if product.quantity < cart_data.quantity:
        raise HTTPException(status_code=400, detail="Not enough product quantity in stock")

    cart_item.quantity = cart_data.quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item


def delete_cart_item(db: Session, user: models.User, item_id: int) -> None:
    cart_item = get_cart_item_by_id(db, user, item_id)
    db.delete(cart_item)
    db.commit()


def clear_cart(db: Session, user: models.User) -> None:
    cart_items = db.query(models.CartItem).filter(models.CartItem.user_id == user.id).all()
    for cart_item in cart_items:
        db.delete(cart_item)
    db.commit()
