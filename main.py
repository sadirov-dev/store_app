from fastapi import FastAPI

from store_app.api.auth import router as auth_router
from store_app.api.cart import router as cart_router
from store_app.api.categories import router as categories_router
from store_app.api.orders import router as orders_router
from store_app.api.products import router as products_router
from store_app.config import get_settings
from store_app.database.db import Base, engine


settings = get_settings()
app = FastAPI(title=settings.app_name)

# This helps when someone runs the app before Alembic migrations.
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(categories_router)
app.include_router(products_router)
app.include_router(cart_router)
app.include_router(orders_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
