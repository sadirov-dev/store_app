from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from store_app.api.dependencies import get_current_user
from store_app.database.db import get_db
from store_app.database.schemas import OrderResponse
from store_app.services.order_service import create_order, get_user_order_by_id, get_user_orders


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, status_code=201)
def create_order_view(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return create_order(db, current_user)


@router.get("", response_model=list[OrderResponse])
def get_orders_view(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_orders(db, current_user)


@router.get("/{order_id}", response_model=OrderResponse)
def get_order_view(order_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return get_user_order_by_id(db, current_user, order_id)
