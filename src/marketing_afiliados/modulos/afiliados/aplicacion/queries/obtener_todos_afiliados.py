from typing import Optional
from src.marketing_afiliados.seedwork.aplicacion.queries import Query
from ..dto import AfiliadoDTO
from ...dominio.objetos_valor import EstadoAfiliado, TipoAfiliado


class ObtenerTodosAfiliados(Query):
    """Query para obtener todos los afiliados con filtros opcionales."""
    
    def __init__(self, 
                 estado: Optional[EstadoAfiliado] = None,
                 tipo: Optional[TipoAfiliado] = None,
                 categoria: Optional[str] = None,
                 limite: int = 100,
                 offset: int = 0):
        super().__init__()
        self.estado = estado
        self.tipo = tipo
        self.categoria = categoria
        self.limite = limite
        self.offset = offset
