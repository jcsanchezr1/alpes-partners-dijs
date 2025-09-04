from src.alpes_partners.seedwork.aplicacion.comandos import Comando


class DesactivarInfluencer(Comando):
    """Comando para desactivar un influencer."""
    
    def __init__(self, influencer_id: str, motivo: str):
        super().__init__()
        self.influencer_id = influencer_id
        self.motivo = motivo
