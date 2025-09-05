"""
Comando para crear una nueva campaña.
"""

from datetime import datetime
from typing import List, Optional
from alpes_partners.seedwork.aplicacion.comandos import Comando


class CrearCampana(Comando):
    """Comando para crear una nueva campaña."""
    
    def __init__(self,
                 nombre: str,
                 descripcion: str,
                 tipo_comision: str,  # 'cpa', 'cpl', 'cpc'
                 valor_comision: float,
                 moneda: str,
                 fecha_inicio: datetime,
                 fecha_fin: Optional[datetime] = None,
                 titulo_material: str = "",
                 descripcion_material: str = "",
                 categorias_objetivo: List[str] = None,
                 tipos_afiliado_permitidos: List[str] = None,
                 paises_permitidos: List[str] = None,
                 enlaces_material: List[str] = None,
                 imagenes_material: List[str] = None,
                 banners_material: List[str] = None,
                 metricas_minimas: dict = None,
                 auto_activar: bool = False,
                 influencer_origen_id: Optional[str] = None,  # Para campañas creadas automáticamente
                 categoria_origen: Optional[str] = None):  # Categoría que originó la campaña
        
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_comision = tipo_comision
        self.valor_comision = valor_comision
        self.moneda = moneda
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.titulo_material = titulo_material
        self.descripcion_material = descripcion_material
        self.categorias_objetivo = categorias_objetivo or []
        self.tipos_afiliado_permitidos = tipos_afiliado_permitidos or []
        self.paises_permitidos = paises_permitidos or []
        self.enlaces_material = enlaces_material or []
        self.imagenes_material = imagenes_material or []
        self.banners_material = banners_material or []
        self.metricas_minimas = metricas_minimas or {}
        self.auto_activar = auto_activar
        self.influencer_origen_id = influencer_origen_id
        self.categoria_origen = categoria_origen


class CrearCampanaPorCategoria(Comando):
    """Comando específico para crear campañas automáticamente basadas en categorías de influencers."""
    
    def __init__(self,
                 influencer_id: str,
                 nombre_influencer: str,
                 email_influencer: str,
                 categorias_influencer: List[str],
                 fecha_registro_influencer: datetime):
        
        self.influencer_id = influencer_id
        self.nombre_influencer = nombre_influencer
        self.email_influencer = email_influencer
        self.categorias_influencer = categorias_influencer
        self.fecha_registro_influencer = fecha_registro_influencer
