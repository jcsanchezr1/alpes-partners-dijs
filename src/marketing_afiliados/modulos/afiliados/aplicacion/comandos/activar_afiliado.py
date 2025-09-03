from src.marketing_afiliados.seedwork.aplicacion.comandos import Comando


class ActivarAfiliado(Comando):
    """Comando para activar un afiliado."""
    
    def __init__(self, afiliado_id: str):
        super().__init__()
        self.afiliado_id = afiliado_id
