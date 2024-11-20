from http import HTTPStatus
from http.client import HTTPException

from fastapi import APIRouter

router = APIRouter(prefix='/api/products', tags=['products'])

products = {
    "status_code": 200,
    "body": {
        "products": [
            {
                "id": 1,
                "price": 100.99,
                "image": "image.jpg",
                "brand": "brand1",
                "title": "tenis",
                "reviewScore": 5.0
            },
            {
                "id": 2,
                "price": 99.99,
                "image": "image.jpg",
                "brand": "brand2",
                "title": "camisa",
                "reviewScore": 4.0
            },
            {
                "id": 3,
                "price": 87.99,
                "image": "image.jpg",
                "brand": "brand4",
                "title": "bermuda",
                "reviewScore": 3.9
            },
            {
                "id": 4,
                "price": 10.99,
                "image": "image.jpg",
                "brand": "brand4",
                "title": "bone",
                "reviewScore": 2.4
            }
        ]
    }
}

@router.get("/", status_code=HTTPStatus.FOUND)
def get_products_list():
    return products

@router.get("/{product_id}")
def get_product_by_id(product_id: int):
    try:
        products_list = products["body"]["products"]
        for product in products_list:
            if product.get("id") == product_id:
                return product
    except Exception:
        raise HTTPStatus.NOT_FOUND
