from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from store_app.database import models, schemas
from store_app.services.category_service import get_category_by_id


def create_product(db: Session, product_data: schemas.ProductCreate) -> models.Product:
    get_category_by_id(db, product_data.category_id)

    product = models.Product(
        title=product_data.title,
        description=product_data.description,
        price=product_data.price,
        quantity=product_data.quantity,
        category_id=product_data.category_id,
        image_url=product_data.image_url,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_products(
    db: Session,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
) -> list[models.Product]:
    query = db.query(models.Product)

    if search:
        query = query.filter(models.Product.title.ilike(f"%{search}%"))
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)

    return query.order_by(models.Product.id.desc()).all()


def get_product_by_id(db: Session, product_id: int) -> models.Product:
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def update_product(db: Session, product_id: int, product_data: schemas.ProductUpdate) -> models.Product:
    product = get_product_by_id(db, product_id)

    if product_data.category_id is not None:
        get_category_by_id(db, product_data.category_id)
        product.category_id = product_data.category_id
    if product_data.title is not None:
        product.title = product_data.title
    if product_data.description is not None:
        product.description = product_data.description
    if product_data.price is not None:
        product.price = product_data.price
    if product_data.quantity is not None:
        product.quantity = product_data.quantity
    if product_data.image_url is not None:
        product.image_url = product_data.image_url

    db.commit()
    db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> None:
    product = get_product_by_id(db, product_id)
    db.delete(product)
    db.commit()
