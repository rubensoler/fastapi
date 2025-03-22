from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Product
from schemas import ProductSchema, CreateProductSchema, UpdateProductSchema
from crud import get_all_products, create_product, update_product, delete_product
from typing import List

router = APIRouter()

@router.get("/")
def root():
    return {"msg": "ok"}

@router.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    return get_all_products(db)

@router.put("/products/{product_id}")
def update_product_route(product_id: int, updated_product: UpdateProductSchema, db: Session = Depends(get_db)):
    product = update_product(db, product_id, updated_product)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto actualizado correctamente"}

@router.post("/products")
def add_product_route(product: CreateProductSchema, db: Session = Depends(get_db)):
    return create_product(db, product)

@router.delete("/products/{product_id}")
def delete_product_route(product_id: int, db: Session = Depends(get_db)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Producto eliminado correctamente"}
