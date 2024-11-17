from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.controllers import products_controller
from app.schemas.product_schema import Product


router = APIRouter(prefix='/api/products', tags=['products'])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", status_code=HTTPStatus.CREATED)
def create_products(request: Product, session: Session = Depends(get_db)):
    return products_controller.create_product(session=session, request=request)

@router.get("/", status_code=HTTPStatus.FOUND)
def get_all_products(page: int = Query(1, ge=1), session: Session = Depends(get_db)):
    products = products_controller.get_products(session=session, page=page)
    return {
        "page": page,
        "products": products
    }

@router.get("/{product_id}", status_code=HTTPStatus.FOUND)
def get_products(product_id: int, session: Session = Depends(get_db)):
    product = products_controller.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Product not found")
    return product

@router.patch("/{product_id}", status_code=HTTPStatus.ACCEPTED)
def update_product(product_id: int, request: Product, session: Session = Depends(get_db)):
    return products_controller.update_user(session=session, product_id=product_id, request=request)

@router.delete("/{product_id}", status_code=HTTPStatus.OK)
def delete_product(product_id: int, session: Session = Depends(get_db)):
    return products_controller.delete_product(session, product_id=product_id)
