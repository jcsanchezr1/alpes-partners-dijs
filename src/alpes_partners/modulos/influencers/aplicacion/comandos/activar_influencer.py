from src.alpes_partners.seedwork.aplicacion.comandos import Comando


class ActivarInfluencer(Comando):
    """Comando para activar un influencer."""
    
    def __init__(self, influencer_id: str):
        super().__init__()
        self.influencer_id = influencer_id
