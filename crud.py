from sqlalchemy.orm import Session
from models import Product
from schemas import CreateProductSchema, UpdateProductSchema

def get_all_products(db: Session):
    return db.query(Product).all()

def get_product_by_id(db: Session, product_id: int):
    return db.query(Product).filter(Product.id == product_id).first()

def create_product(db: Session, product: CreateProductSchema):
    new_product = Product(name=product.name, price=product.price, image_url=product.image_url)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

def update_product(db: Session, product_id: int, updated_product: UpdateProductSchema):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    product.name = updated_product.name
    product.price = updated_product.price
    product.image_url = updated_product.image_url
    db.commit()
    return product

def delete_product(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    db.delete(product)
    db.commit()
    return product
