from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from store_app.database.db import get_db
from store_app.database.schemas import CategoryCreate, CategoryResponse, CategoryUpdate
from store_app.services.category_service import (
    create_category,
    delete_category,
    get_categories,
    get_category_by_id,
    update_category,
)


router = APIRouter(prefix="/api/categories", tags=["Categories"])


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category_view(category_data: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category_data)


@router.get("", response_model=list[CategoryResponse])
def get_categories_view(db: Session = Depends(get_db)):
    return get_categories(db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category_view(category_id: int, db: Session = Depends(get_db)):
    return get_category_by_id(db, category_id)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category_view(category_id: int, category_data: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category(db, category_id, category_data)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category_view(category_id: int, db: Session = Depends(get_db)):
    delete_category(db, category_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
