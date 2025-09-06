# AlpesPartners DIJS

Sistema de **AlpesPartners** implementado con **Domain-Driven Design (DDD)** y **arquitectura hexagonal (puertos y adaptadores)** basada en eventos.

## 🏗️ Arquitectura

### Arquitectura Hexagonal (Puertos y Adaptadores)

Este proyecto implementa una **arquitectura hexagonal** que separa claramente las responsabilidades y permite alta testabilidad y mantenibilidad:

#### **Núcleo del Dominio (Hexágono Central)**
- **Entidades**: Agregados raíz con lógica de negocio (`Influencer`)
- **Objetos Valor**: Tipos inmutables (`Email`, `Telefono`, `EstadoInfluencer`)
- **Eventos de Dominio**: Comunicación entre contextos (`InfluencerRegistrado`)
- **Excepciones de Dominio**: Reglas de negocio (`EmailYaRegistrado`)
- **Repositorios (Puertos)**: Interfaces abstractas para persistencia

#### **Puertos (Interfaces)**
- **`RepositorioInfluencers`**: Puerto para persistencia de influencers
- **`UnidadTrabajo`**: Puerto para manejo de transacciones
- **`ManejadorComando`**: Puerto para procesamiento de comandos

#### **Adaptadores (Implementaciones)**
- **`RepositorioInfluencersSQLAlchemy`**: Adaptador de persistencia con SQLAlchemy
- **`DespachadorInfluencers`**: Adaptador de mensajería con Apache Pulsar
- **`InfluencerMapper`**: Adaptador de conversión entidad ↔ modelo
- **API REST**: Adaptador de entrada HTTP

### Principios DDD Implementados

El servicio utiliza los siguientes **patrones y principios de Domain-Driven Design**:

- ** Entidades**: Objetos con identidad única y ciclo de vida (`Influencer`)
- ** Objetos Valor**: Tipos inmutables que representan conceptos (`Email`, `Telefono`)
- ** Seedwork**: Elementos base compartidos entre módulos
- ** Servicios de Dominio**: Lógica que no pertenece a una entidad específica
- ** Módulos**: Separación de contextos acotados (`influencers`, `campanas`)
- ** Agregaciones**: Raíces de agregado que mantienen consistencia
- ** Fábricas**: Creación de objetos complejos
- ** Repositorios**: Abstracción para persistencia
- ** Unidad de Trabajo**: Manejo de transacciones y eventos

## 🏢 Estructura del Proyecto

```
src/alpes_partners/
├── seedwork/                    # Base DDD compartida
│   ├── dominio/                 # Entidades, eventos, repositorios base
│   ├── aplicacion/              # Comandos, handlers, DTOs base
│   ├── infraestructura/         # UoW, base de datos, eventos
│   └── presentacion/            # API base
├── modulos/
│   ├── influencers/             # Módulo Influencers
│   │   ├── dominio/             # Entidades, objetos valor, eventos
│   │   ├── aplicacion/          # Comandos, handlers, servicios
│   │   └── infraestructura/     # Repositorios, despachadores
│   └── campanas/                # Módulo Campañas
│       ├── dominio/             # Entidades, objetos valor, eventos
│       ├── aplicacion/          # Comandos, handlers, servicios
│       └── infraestructura/     # Repositorios, consumidores
├── config/                      # Configuración
└── api/                         # Endpoints REST
```

## Manejador de Base de Datos

### Persistencia y Consulta de Datos

El sistema utiliza **SQLAlchemy** como ORM para la persistencia:

- **Modelos**: Representación de tablas de base de datos (`InfluencerModelo`)
- **Mappers**: Conversión entre entidades de dominio y modelos de BD
- **Repositorios**: Implementaciones concretas de puertos de persistencia
- **Unidad de Trabajo**: Manejo de transacciones y eventos post-commit

```python
# Ejemplo de flujo de persistencia
repositorio = RepositorioInfluencersSQLAlchemy()
uow = UnidadTrabajoSQLAlchemy()

# Registrar operación en UoW
uow.registrar_batch(repositorio.agregar, influencer)
uow.commit()  # Persiste y publica eventos
```

## 📡omunicación Entre Módulos

La **comunicación entre módulos** (`influencers` ↔ `campanas`) se realiza **exclusivamente mediante eventos de dominio**:

### Flujo de Eventos
1. **Módulo Influencers** emite `InfluencerRegistrado`
2. **Apache Pulsar** transporta el evento al tópico `eventos-influencers`
3. **Módulo Campañas** consume el evento y reacciona según su lógica de negocio

### Eventos Implementados
- **`InfluencerRegistrado`**: Notifica que un nuevo influencer se ha registrado
- **`CampanaCreada`**: Notifica la creación de una nueva campaña

## Patrón CQS (Command Query Separation)

El sistema implementa **CQS** para separar claramente comandos y consultas:

### **Comandos** (Modifican Estado)
- **`RegistrarInfluencer`**: Registra un nuevo influencer
- **`CrearCampana`**: Crea una nueva campaña
- Procesados por **Command Handlers** específicos

### **Queries** (Solo Lectura)
- **`ListarInfluencers`**: Consulta influencers con filtros
- Procesados por **servicios de aplicación**

### **Eventos** (Notificaciones)
- **`InfluencerRegistrado`**: Evento de dominio
- **`CampanaCreada`**: Evento de dominio
- Procesados por **Event Handlers** y despachadores

## Inicio del Flujo

### Endpoint de Registro de Influencer

**URL**: `POST /influencers/registrar-comando`

**Body de Ejemplo**:
```json
{
    "nombre": "Ana García",
    "email": "ana.garcia1@example.com",
    "categorias": ["moda", "juegos"],
    "descripcion": "Influencer de moda y lifestyle con enfoque en sostenibilidad",
    "biografia": "Creadora de contenido apasionada por la moda sostenible",
    "sitio_web": "https://anagarcia.com",
    "telefono": "+34123456789"
}
```

### Flujo Completo
1. **API** recibe HTTP POST
2. **Comando** `RegistrarInfluencer` se crea y ejecuta
3. **Handler** procesa el comando
4. **Entidad** `Influencer` se crea y emite evento
5. **UoW** persiste en BD y publica evento a Pulsar
6. **Módulo Campañas** consume evento y reacciona

## Tecnologías

- **Python 3.9+** - Lenguaje de programación
- **Flask 3.0+** - Framework web
- **SQLAlchemy 2.0+** - ORM para persistencia
- **Apache Pulsar 3.7** - Broker de mensajes y eventos
- **PostgreSQL** - Base de datos relacional
- **Docker & Docker Compose** - Containerización
- **Pydispatch** - Manejo de eventos internos
- **Avro Schema** - Serialización de eventos

## Instalación y Ejecución

### Levantar el Proyecto

```bash
# Clonar el repositorio
git clone <repo-url>
cd alpes-partners-dijs

# Levantar todos los servicios con Docker
docker-compose up --build -d
```

### Servicios Incluidos
- **alpes-partners**: Aplicación Flask
- **PostgreSQL**: Base de datos
- **Apache Pulsar**: Broker de mensajes

### Desarrollo Local

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp env.example .env

# Ejecutar aplicación Flask
python run_flask.py

# Ejecutar consumidor de Pulsar (en otra terminal)
python run_pulsar_consumer.py
```

## 📋 API Endpoints

### Influencers
- **`POST /influencers/registrar-comando`** - Registrar influencer (asíncrono)
- **`GET /influencers/`** - Listar influencers con filtros opcionales