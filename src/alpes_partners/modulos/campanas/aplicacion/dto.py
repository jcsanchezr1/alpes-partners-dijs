from typing import Optional, Dict, List
from pydantic import BaseModel, validator
from src.alpes_partners.seedwork.aplicacion.dto import DTO
from alpes_partners.modulos.campanas.dominio.objetos_valor import TipoComision, EstadoCampana


class RegistrarCampanaDTO(DTO):
    """DTO para registrar una campana."""
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    descripcion: str
    tipo_comision: str
    valor_comision: float
    moneda: str
    fecha_inicio: str
    fecha_fin: Optional[str] = None
    titulo_material: str = ""
    descripcion_material: str = ""
    categorias_objetivo: Optional[List[str]] = None
    tipos_afiliado_permitidos: Optional[List[str]] = None
    paises_permitidos: Optional[List[str]] = None
    enlaces_material: Optional[List[str]] = None
    imagenes_material: Optional[List[str]] = None
    banners_material: Optional[List[str]] = None
    metricas_minimas: Optional[dict] = None
    auto_activar: bool = False
    influencer_origen_id: Optional[str] = None
    categoria_origen: Optional[str] = None
    
    @validator('nombre')
    def validar_nombre(cls, v):
        if not v or not v.strip():
            raise ValueError('El nombre es requerido')
        return v.strip()
    
    @validator('descripcion')
    def validar_descripcion(cls, v):
        if not v or not v.strip():
            raise ValueError('La descripción es requerida')
        return v.strip()
    
    @validator('tipo_comision')
    def validar_tipo_comision(cls, v):
        if v not in ['cpa', 'cpl', 'cpc']:
            raise ValueError('Tipo de comisión inválido. Debe ser: cpa, cpl o cpc')
        return v.lower()
    
    @validator('valor_comision')
    def validar_valor_comision(cls, v):
        if v <= 0:
            raise ValueError('El valor de comisión debe ser mayor a 0')
        return v
    
    @validator('categorias_objetivo', 'tipos_afiliado_permitidos', 'paises_permitidos', 
               'enlaces_material', 'imagenes_material', 'banners_material', pre=True)
    def validar_listas(cls, v):
        return v or []
    
    @validator('metricas_minimas', pre=True)
    def validar_metricas_minimas(cls, v):
        return v or {}


class CampanaDTO(DTO):
    """DTO para representar una campana."""
    id: str
    nombre: str
    descripcion: str
    estado: str
    tipo_comision: str
    valor_comision: float
    moneda: str
    fecha_inicio: str
    fecha_fin: Optional[str] = None
    fecha_creacion: str
    fecha_activacion: Optional[str] = None
    
    # Material promocional
    titulo_material: str = ""
    descripcion_material: str = ""
    enlaces_material: List[str] = []
    imagenes_material: List[str] = []
    banners_material: List[str] = []
    
    # Criterios de afiliado
    categorias_objetivo: List[str] = []
    tipos_afiliado_permitidos: List[str] = []
    paises_permitidos: List[str] = []
    metricas_minimas: dict = {}
    
    # Métricas
    afiliados_activos: int = 0
    conversiones_totales: int = 0
    ingresos_generados: float = 0.0
    
    # Origen
    influencer_origen_id: Optional[str] = None
    categoria_origen: Optional[str] = None


class ActualizarCampanaDTO(DTO):
    """DTO para actualizar una campana."""
    descripcion: Optional[str] = None
    valor_comision: Optional[float] = None
    fecha_fin: Optional[str] = None
    titulo_material: Optional[str] = None
    descripcion_material: Optional[str] = None
    
    @validator('valor_comision')
    def validar_valor_comision(cls, v):
        if v is not None and v <= 0:
            raise ValueError('El valor de comisión debe ser mayor a 0')
        return v


class AgregarMaterialDTO(DTO):
    """DTO para agregar material promocional a una campana."""
    enlaces: List[str] = []
    imagenes: List[str] = []
    banners: List[str] = []


class ActualizarCriteriosDTO(DTO):
    """DTO para actualizar criterios de afiliado."""
    tipos_afiliado_permitidos: Optional[List[str]] = None
    paises_permitidos: Optional[List[str]] = None
    metricas_minimas: Optional[dict] = None


class ActualizarMetricasCampanaDTO(DTO):
    """DTO para actualizar métricas de campana."""
    afiliados_activos: Optional[int] = 0
    conversiones_totales: Optional[int] = 0
    ingresos_generados: Optional[float] = 0.0
    
    @validator('afiliados_activos')
    def validar_afiliados(cls, v):
        if v is not None and v < 0:
            raise ValueError('Los afiliados activos no pueden ser negativos')
        return v
    
    @validator('conversiones_totales')
    def validar_conversiones(cls, v):
        if v is not None and v < 0:
            raise ValueError('Las conversiones totales no pueden ser negativas')
        return v
    
    @validator('ingresos_generados')
    def validar_ingresos(cls, v):
        if v is not None and v < 0:
            raise ValueError('Los ingresos generados no pueden ser negativos')
        return v
