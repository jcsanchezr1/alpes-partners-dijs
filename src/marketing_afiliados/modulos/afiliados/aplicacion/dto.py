from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr, validator
from src.marketing_afiliados.seedwork.aplicacion.dto import DTO
from ..dominio.objetos_valor import TipoAfiliado, EstadoAfiliado


class RegistrarAfiliadoDTO(DTO):
    """DTO para registrar un afiliado."""
    nombre: str
    email: EmailStr
    tipo_afiliado: TipoAfiliado
    categorias: List[str]
    descripcion: str
    sitio_web: Optional[str] = ""
    telefono: Optional[str] = ""
    redes_sociales: Optional[Dict[str, str]] = None
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre es requerido')
        return v.strip()
    
    @validator('categorias')
    def validar_categorias(cls, v):
        if not v:
            raise ValueError('Debe especificar al menos una categoría')
        return v
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if not v or not v.strip():
            raise ValueError('La descripción es requerida')
        return v.strip()


class AfiliadoDTO(DTO):
    """DTO para representar un afiliado."""
    id: str
    nombre: str
    email: str
    tipo_afiliado: TipoAfiliado
    estado: EstadoAfiliado
    categorias: List[str]
    descripcion: str
    sitio_web: Optional[str] = ""
    telefono: Optional[str] = ""
    redes_sociales: Optional[Dict[str, str]] = None
    fecha_creacion: str
    fecha_activacion: Optional[str] = None
    clics_totales: int = 0
    conversiones_totales: int = 0
    ingresos_generados: float = 0.0
    tasa_conversion: float = 0.0


class ActualizarPerfilAfiliadoDTO(DTO):
    """DTO para actualizar perfil de afiliado."""
    descripcion: Optional[str] = None
    sitio_web: Optional[str] = None
    redes_sociales: Optional[Dict[str, str]] = None
