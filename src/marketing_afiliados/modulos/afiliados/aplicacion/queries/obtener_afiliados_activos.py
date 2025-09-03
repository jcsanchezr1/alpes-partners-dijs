from typing import Optional
from src.marketing_afiliados.seedwork.aplicacion.queries import Query
from ...dominio.objetos_valor import TipoAfiliado


class ObtenerAfiliadosActivos(Query):
    """Query para obtener afiliados activos."""
    
    def __init__(self, 
                 tipo: Optional[TipoAfiliado] = None,
                 categoria: Optional[str] = None,
                 limite: int = 100,
                 offset: int = 0):
        super().__init__()
        self.tipo = tipo
        self.categoria = categoria
        self.limite = limite
        self.offset = offset
