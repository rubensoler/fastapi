from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from typing import List
import os

# 🔹 Definir la ruta absoluta de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'products.db')}"
print(f"📢 Base de datos usada: {DATABASE_URL}")  # 🔴 Debugging

# 🔹 Configuración de la base de datos SQLite
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔹 Modelo de la base de datos
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)
    image_url = Column(String)

# 🔹 Crear la base de datos si no existe
if not os.path.exists(os.path.join(BASE_DIR, "products.db")):
    print("📢 Base de datos no encontrada. Creando nueva base de datos...")
Base.metadata.create_all(bind=engine)

# 🔹 Inicialización de FastAPI
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

# 🔹 Configurar CORS para permitir peticiones desde React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las URLs (puedes restringirlo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Permite todos los headers
)

# 🔹 Modelos Pydantic para validación de datos
class ProductSchema(BaseModel):
    id: int
    name: str
    price: float
    image_url: str

    class Config:
        from_attributes = True

class CreateProductSchema(BaseModel):
    name: str
    price: float
    image_url: str

class UpdateProductSchema(BaseModel):
    name: str
    price: float
    image_url: str

# 🔹 Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔹 Endpoint para obtener todos los productos
@app.get("/products", response_model=List[ProductSchema])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    print(f"📢 Productos en la BD: {products}")  # 🔴 Debugging
    return products

# 🔹 Endpoint para actualizar solo el precio de un producto
@app.put("/products/{product_id}")
def update_product(product_id: int, updated_product: UpdateProductSchema, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    product.name = updated_product.name
    product.price = updated_product.price
    product.image_url = updated_product.image_url
    db.commit()
    return {"message": "Producto actualizado correctamente"}

# 🔹 Endpoint para agregar un nuevo producto
@app.post("/products")
def add_product(product: CreateProductSchema, db: Session = Depends(get_db)):
    new_product = Product(name=product.name, price=product.price, image_url=product.image_url)
    db.add(new_product)
    db.commit()
    return {"message": "Producto agregado exitosamente"}

# 🔹 Endpoint para eliminar un producto
@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(product)
    db.commit()
    return {"message": "Producto eliminado correctamente"}


