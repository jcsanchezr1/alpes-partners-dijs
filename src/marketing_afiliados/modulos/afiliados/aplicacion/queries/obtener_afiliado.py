from src.marketing_afiliados.seedwork.aplicacion.queries import Query


class ObtenerAfiliado(Query):
    """Query para obtener un afiliado por ID."""
    
    def __init__(self, afiliado_id: str):
        super().__init__()
        self.afiliado_id = afiliado_id


class ObtenerAfiliadoPorEmail(Query):
    """Query para obtener un afiliado por email."""
    
    def __init__(self, email: str):
        super().__init__()
        self.email = email
