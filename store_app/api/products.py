from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from store_app.database.db import get_db
from store_app.database.schemas import ProductCreate, ProductResponse, ProductUpdate
from store_app.services.product_service import (
    create_product,
    delete_product,
    get_product_by_id,
    get_products,
    update_product,
)


router = APIRouter(prefix="/api/products", tags=["Products"])


@router.post("", response_model=ProductResponse, status_code=201)
def create_product_view(product_data: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product_data)


@router.get("", response_model=list[ProductResponse])
def get_products_view(
    search: Optional[str] = Query(default=None),
    category_id: Optional[int] = Query(default=None),
    min_price: Optional[float] = Query(default=None),
    max_price: Optional[float] = Query(default=None),
    db: Session = Depends(get_db),
):
    return get_products(db, search, category_id, min_price, max_price)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product_view(product_id: int, db: Session = Depends(get_db)):
    return get_product_by_id(db, product_id)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product_view(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product_view(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
