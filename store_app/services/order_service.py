from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from store_app.database import models


def create_order(db: Session, user: models.User) -> models.Order:
    cart_items = (
        db.query(models.CartItem)
        .options(joinedload(models.CartItem.product))
        .filter(models.CartItem.user_id == user.id)
        .all()
    )
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    total_price = 0.0
    order = models.Order(user_id=user.id, total_price=0)
    db.add(order)
    db.flush()

    for cart_item in cart_items:
        product = cart_item.product
        if product.quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Not enough quantity for product {product.title}",
            )

        product.quantity -= cart_item.quantity
        item_price = product.price * cart_item.quantity
        total_price += item_price

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price,
        )
        db.add(order_item)
        db.delete(cart_item)

    order.total_price = total_price
    db.commit()
    db.refresh(order)
    return order


def get_user_orders(db: Session, user: models.User) -> list[models.Order]:
    return (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.user_id == user.id)
        .order_by(models.Order.id.desc())
        .all()
    )


def get_user_order_by_id(db: Session, user: models.User, order_id: int) -> models.Order:
    order = (
        db.query(models.Order)
        .options(joinedload(models.Order.items))
        .filter(models.Order.id == order_id, models.Order.user_id == user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
