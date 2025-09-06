from typing import Optional, Dict, List
from pydantic import BaseModel, EmailStr, validator
from src.alpes_partners.seedwork.aplicacion.dto import DTO
from ..dominio.objetos_valor import TipoInfluencer, EstadoInfluencer, Plataforma, Genero, RangoEdad


class RegistrarInfluencerDTO(DTO):
    """DTO para registrar un influencer."""
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    email: EmailStr
    categorias: List[str]
    descripcion: str
    biografia: Optional[str] = ""
    sitio_web: Optional[str] = ""
    telefono: Optional[str] = ""
    
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


class DatosAudienciaDTO(DTO):
    """DTO para datos de audiencia de una plataforma."""
    plataforma: Plataforma
    seguidores: int
    engagement_rate: float
    alcance_promedio: Optional[int] = 0
    
    @validator('seguidores')
    def validar_seguidores(cls, v):
        if v < 0:
            raise ValueError('Los seguidores no pueden ser negativos')
        return v
    
    @validator('engagement_rate')
    def validar_engagement(cls, v):
        if not (0 <= v <= 100):
            raise ValueError('El engagement rate debe estar entre 0 y 100')
        return v
    
    @validator('plataforma', pre=True)
    def validar_plataforma(cls, v):
        if isinstance(v, str):
            try:
                return Plataforma(v)
            except ValueError:
                raise ValueError(f'Plataforma inválida: {v}')
        return v


class DemografiaDTO(DTO):
    """DTO para demografía de audiencia."""
    distribucion_genero: Dict[Genero, float]
    distribucion_edad: Dict[RangoEdad, float]
    paises_principales: List[str]
    
    @validator('distribucion_genero')
    def validar_distribucion_genero(cls, v):
        if abs(sum(v.values()) - 100.0) > 1.0:
            raise ValueError('La distribución de género debe sumar 100%')
        return v
    
    @validator('distribucion_edad')
    def validar_distribucion_edad(cls, v):
        if abs(sum(v.values()) - 100.0) > 1.0:
            raise ValueError('La distribución de edad debe sumar 100%')
        return v


class InfluencerDTO(DTO):
    """DTO para representar un influencer."""
    id: str
    nombre: str
    email: str
    estado: EstadoInfluencer
    categorias: List[str]
    descripcion: str
    biografia: Optional[str] = ""
    sitio_web: Optional[str] = ""
    telefono: Optional[str] = ""
    fecha_creacion: str
    fecha_activacion: Optional[str] = None
    
    # Datos de audiencia
    plataformas: List[str] = []
    total_seguidores: int = 0
    engagement_promedio: float = 0.0
    tipo_principal: Optional[str] = None
    
    # Métricas
    campanas_completadas: int = 0
    cpm_promedio: float = 0.0
    ingresos_generados: float = 0.0
    
    # Demografia (opcional)
    demografia: Optional[DemografiaDTO] = None


class ActualizarPerfilInfluencerDTO(DTO):
    """DTO para actualizar perfil de influencer."""
    descripcion: Optional[str] = None
    biografia: Optional[str] = None
    sitio_web: Optional[str] = None


class AgregarPlataformaDTO(DTO):
    """DTO para agregar una plataforma al influencer."""
    datos_audiencia: DatosAudienciaDTO


class ActualizarMetricasDTO(DTO):
    """DTO para actualizar métricas del influencer."""
    campanas_completadas: Optional[int] = 0
    engagement_promedio: Optional[float] = 0.0
    cpm_promedio: Optional[float] = 0.0
    ingresos: Optional[float] = 0.0
    
    @validator('campanas_completadas')
    def validar_campanas(cls, v):
        if v is not None and v < 0:
            raise ValueError('Las campanas completadas no pueden ser negativas')
        return v
    
    @validator('engagement_promedio')
    def validar_engagement(cls, v):
        if v is not None and v < 0:
            raise ValueError('El engagement promedio no puede ser negativo')
        return v
    
    @validator('cpm_promedio')
    def validar_cpm(cls, v):
        if v is not None and v < 0:
            raise ValueError('El CPM promedio no puede ser negativo')
        return v
    
    @validator('ingresos')
    def validar_ingresos(cls, v):
        if v is not None and v < 0:
            raise ValueError('Los ingresos no pueden ser negativos')
        return v
