import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 🔹 Solo carga .env si no estás en producción
from dotenv import load_dotenv
if os.getenv("ENV") != "production":
    load_dotenv()

# 🔹 Leer la variable de entorno DATABASE_URL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ ERROR: La variable de entorno DATABASE_URL no está configurada.")

# 🔹 Configuración condicional si es SQLite
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# 🔹 Crear el motor
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# 🔹 Crear la sesión y el Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 🔹 Dependencia para FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
