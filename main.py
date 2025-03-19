from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import products

# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)

# Inicialización de FastAPI con configuración de documentación
app = FastAPI(
    title="Mi API FastAPI",
    description="API desplegada en Railway",
    version="1.0",
    docs_url="/docs",  # Habilita la documentación en /docs
    redoc_url="/redoc"  # Habilita la documentación alternativa en /redoc
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir las rutas
app.include_router(products.router)

