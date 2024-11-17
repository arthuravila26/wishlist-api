from sqlalchemy.orm import Session
from app.models.products import Products
from app.utils.exceptions import ProductNotFound
from app.utils.logger import logger

def create_product(session: Session, request):
    product = Products(title=request.title, price=request.price, image=request.image, brand=request.brand, reviewScore=request.reviewScore)
    session.add(product)
    session.commit()
    session.refresh(product)
    logger.info(f'Product {request.title} has been created.')
    return product

def get_products(session: Session, page: int = 1):
    per_page = 5
    offset = (page - 1) * per_page
    return session.query(Products).offset(offset).limit(per_page).all()

def get_product_by_id(session: Session, product_id: int):
    return session.query(Products).filter(Products.id == product_id).first()

def update_user(session: Session, product_id: int, request):
    try:
        product = get_product_by_id(session, product_id)
        product.title = request.title
        product.price = request.price
        product.brand = request.brand
        product.image = request.image
        product.reviewScore = request.reviewScore
        product.commit()
        product.refresh(product)
        logger.error(f'Product {request.title} Updated.')
        return product
    except:
        logger.error(f'Product {request.title} Not found.')
        raise ProductNotFound()

def delete_product(session: Session, product_id: int):
    try:
        product = get_product_by_id(session, product_id)
        session.delete(product)
        session.commit()
        logger.info(f'Product {product.title} Deleted.')
        return {"message": "Product deleted successfully"}
    except:
        logger.error(f'Product {product.name} Not found.')
        raise ProductNotFound()
