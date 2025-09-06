# AlpesPartners DIJS

Sistema de AlpesPartners implementado con Domain-Driven Design (DDD) y arquitectura basada en eventos.

## Arquitectura

Este proyecto implementa el servicio de **AlpesPartners** con dos módulos principales:

- **Módulo Afiliados**: Gestión del ciclo de vida de afiliados
- **Módulo Campanas**: Gestión de campanas de afiliación

## Comunicación Asíncrona

Los módulos se comunican mediante eventos de dominio a través de Redis como broker de mensajes:

- `AfiliadoRegistrado` → Notifica al módulo Campanas
- `CampanaCreada` → Notifica oportunidades a afiliados
- `AfiliadoAsignadoACampana` → Confirma asignaciones

## Tecnologías

- **Python 3.11+**
- **FastAPI** - API REST
- **SQLAlchemy** - ORM
- **Redis** - Broker de mensajes
- **Celery** - Procesamiento asíncrono
- **PostgreSQL** - Base de datos
- **Docker** - Containerización

## Instalación

### Con Docker (Recomendado)

```bash
# Clonar el repositorio
git clone <repo-url>
cd alpespartners_dijs

# Levantar servicios
docker-compose up -d
```

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn src.alpes_partners.main:app --reload
```

## API Endpoints

### Afiliados
- `POST /api/v1/afiliados` - Registrar afiliado
- `GET /api/v1/afiliados` - Listar afiliados
- `GET /api/v1/afiliados/{id}` - Obtener afiliado
- `PUT /api/v1/afiliados/{id}/activar` - Activar afiliado

### Campanas
- `POST /api/v1/campanas` - Crear campana
- `GET /api/v1/campanas` - Listar campanas
- `GET /api/v1/campanas/{id}` - Obtener campana
- `POST /api/v1/campanas/{id}/asignar-afiliado` - Asignar afiliado

## Estructura del Proyecto

```
src/
└── alpes_partners/
    ├── seedwork/           # Base DDD compartida
    ├── modulos/
    │   ├── afiliados/      # Módulo Afiliados
    │   └── campanas/       # Módulo Campanas
    ├── config/             # Configuración
    └── api/                # Endpoints REST
```

## Testing

```bash
# Ejecutar tests
pytest

# Con cobertura
pytest --cov=src
```
