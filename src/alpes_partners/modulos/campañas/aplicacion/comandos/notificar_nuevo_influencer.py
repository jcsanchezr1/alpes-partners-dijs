from typing import List
from ....seedwork.aplicacion.comandos import Comando


class NotificarNuevoInfluencer(Comando):
    """Comando para notificar sobre un nuevo influencer disponible."""
    
    def __init__(self, 
                 influencer_id: str,
                 nombre: str,
                 tipo_influencer: str,
                 categorias: List[str],
                 plataformas: List[str]):
        super().__init__()
        self.influencer_id = influencer_id
        self.nombre = nombre
        self.tipo_influencer = tipo_influencer
        self.categorias = categorias
        self.plataformas = plataformas