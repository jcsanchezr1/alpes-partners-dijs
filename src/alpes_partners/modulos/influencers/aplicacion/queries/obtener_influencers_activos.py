from typing import Optional
from src.alpes_partners.seedwork.aplicacion.queries import Query
from ...dominio.objetos_valor import TipoInfluencer, Plataforma


class ObtenerInfluencersActivos(Query):
    """Query para obtener influencers activos."""
    
    def __init__(self, 
                 tipo: Optional[TipoInfluencer] = None,
                 categoria: Optional[str] = None,
                 plataforma: Optional[Plataforma] = None,
                 min_seguidores: Optional[int] = None,
                 engagement_minimo: Optional[float] = None,
                 limite: int = 100,
                 offset: int = 0):
        super().__init__()
        self.tipo = tipo
        self.categoria = categoria
        self.plataforma = plataforma
        self.min_seguidores = min_seguidores
        self.engagement_minimo = engagement_minimo
        self.limite = limite
        self.offset = offset
