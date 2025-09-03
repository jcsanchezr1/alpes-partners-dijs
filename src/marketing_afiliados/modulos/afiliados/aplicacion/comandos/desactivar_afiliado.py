from src.marketing_afiliados.seedwork.aplicacion.comandos import Comando


class DesactivarAfiliado(Comando):
    """Comando para desactivar un afiliado."""
    
    def __init__(self, afiliado_id: str, motivo: str):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.motivo = motivo
