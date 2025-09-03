from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .config.settings import settings
from .api.afiliados import router as afiliados_router

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Sistema de Marketing de Afiliados con arquitectura DDD y eventos",
    debug=settings.debug
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(afiliados_router)

# Eventos de aplicación
@app.on_event("startup")
async def startup_event():
    """Inicialización de la aplicación."""
    print(f"Iniciando {settings.app_name} v{settings.app_version}")
    print(f"Entorno: {settings.environment}")
    
    # Aquí se inicializarían:
    # - Conexión a base de datos
    # - Consumidores de eventos
    # - Contenedor de dependencias
    # - Migraciones de base de datos


@app.on_event("shutdown")
async def shutdown_event():
    """Limpieza al cerrar la aplicación."""
    print("Cerrando aplicación...")
    
    # Aquí se cerrarían:
    # - Conexiones de base de datos
    # - Consumidores de eventos
    # - Otros recursos


@app.get("/")
async def root():
    """Endpoint de salud básico."""
    return {
        "mensaje": "AlpesPartners DIJS - Marketing de Afiliados API",
        "version": settings.app_version,
        "estado": "activo"
    }


@app.get("/health")
async def health_check():
    """Endpoint de verificación de salud."""
    return {
        "estado": "saludable",
        "version": settings.app_version,
        "entorno": settings.environment
    }


if __name__ == "__main__":
    uvicorn.run(
        "src.marketing_afiliados.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
