from enum import Enum
from typing import List
from src.marketing_afiliados.seedwork.dominio.objetos_valor import ObjetoValor


class TipoAfiliado(Enum):
    """Tipos de afiliados según el texto del negocio."""
    TRADICIONAL = "tradicional"  # Sitios de comparación, cupones, cashback
    INFLUENCER = "influencer"    # Influencers y creadores de contenido
    MEDIO_EDITORIAL = "medio_editorial"  # Revistas y portales de noticias
    EMBAJADOR = "embajador"      # Clientes actuales o empleados
    PARTNER_B2B = "partner_b2b"  # Integradores SaaS
    AGENCIA = "agencia"          # Agencias de partners


class EstadoAfiliado(Enum):
    """Estados posibles de un afiliado."""
    PENDIENTE = "pendiente"
    ACTIVO = "activo"
    INACTIVO = "inactivo"
    SUSPENDIDO = "suspendido"


class CategoriaAfiliado(ObjetoValor):
    """Categorías de productos/servicios que maneja el afiliado."""
    
    def __init__(self, categorias: List[str]):
        if not categorias:
            raise ValueError("Debe tener al menos una categoría")
        self.categorias = [cat.lower().strip() for cat in categorias]


class PerfilAfiliado(ObjetoValor):
    """Perfil completo del afiliado."""
    
    def __init__(self, 
                 tipo: TipoAfiliado,
                 categorias: CategoriaAfiliado,
                 descripcion: str,
                 sitio_web: str = "",
                 redes_sociales: dict = None):
        self.tipo = tipo
        self.categorias = categorias
        self.descripcion = descripcion.strip()
        self.sitio_web = sitio_web.strip()
        self.redes_sociales = redes_sociales or {}
        
        if not self.descripcion:
            raise ValueError("La descripción es requerida")


class MetricasAfiliado(ObjetoValor):
    """Métricas de rendimiento del afiliado."""
    
    def __init__(self, 
                 clics_totales: int = 0,
                 conversiones_totales: int = 0,
                 ingresos_generados: float = 0.0,
                 tasa_conversion: float = 0.0):
        self.clics_totales = max(0, clics_totales)
        self.conversiones_totales = max(0, conversiones_totales)
        self.ingresos_generados = max(0.0, ingresos_generados)
        self.tasa_conversion = max(0.0, min(100.0, tasa_conversion))
    
    def calcular_tasa_conversion(self) -> float:
        """Calcula la tasa de conversión."""
        if self.clics_totales == 0:
            return 0.0
        return (self.conversiones_totales / self.clics_totales) * 100
