from datetime import datetime
from typing import Optional
from sqlalchemy import Column, String, DateTime, Text, JSON, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

from ..dominio.objetos_valor import TipoAfiliado, EstadoAfiliado

Base = declarative_base()


class AfiliadoModelo(Base):
    """Modelo SQLAlchemy para la entidad Afiliado."""
    
    __tablename__ = "afiliados"
    
    # Campos básicos
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    telefono = Column(String(50), nullable=True)
    
    # Perfil
    tipo_afiliado = Column(String(50), nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    categorias = Column(JSON, nullable=False)  # Lista de strings
    descripcion = Column(Text, nullable=False)
    sitio_web = Column(String(500), nullable=True)
    redes_sociales = Column(JSON, nullable=True)  # Dict de string a string
    
    # Métricas
    clics_totales = Column(String, nullable=False, default="0")  # Almacenamos como string para evitar problemas de precisión
    conversiones_totales = Column(String, nullable=False, default="0")
    ingresos_generados = Column(String, nullable=False, default="0.0")
    
    # Fechas
    fecha_creacion = Column(DateTime, nullable=False, default=datetime.utcnow)
    fecha_activacion = Column(DateTime, nullable=True)
    fecha_desactivacion = Column(DateTime, nullable=True)
    
    # Control de versión para optimistic locking
    version = Column(String, nullable=False, default="1")
    
    def __repr__(self):
        return f"<AfiliadoModelo(id={self.id}, nombre='{self.nombre}', email='{self.email}')>"
