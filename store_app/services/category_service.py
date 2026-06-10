from fastapi import HTTPException
from sqlalchemy.orm import Session

from store_app.database import models, schemas


def create_category(db: Session, category_data: schemas.CategoryCreate) -> models.Category:
    existing_category = db.query(models.Category).filter(models.Category.name == category_data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    category = models.Category(name=category_data.name, description=category_data.description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def get_categories(db: Session) -> list[models.Category]:
    return db.query(models.Category).order_by(models.Category.id.desc()).all()


def get_category_by_id(db: Session, category_id: int) -> models.Category:
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def update_category(db: Session, category_id: int, category_data: schemas.CategoryUpdate) -> models.Category:
    category = get_category_by_id(db, category_id)

    if category_data.name and category_data.name != category.name:
        existing_category = db.query(models.Category).filter(models.Category.name == category_data.name).first()
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        category.name = category_data.name

    if category_data.description is not None:
        category.description = category_data.description

    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int) -> None:
    category = get_category_by_id(db, category_id)
    db.delete(category)
    db.commit()
