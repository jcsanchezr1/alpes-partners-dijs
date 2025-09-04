from typing import Optional
from src.alpes_partners.seedwork.aplicacion.comandos import Comando


class ActualizarPerfilInfluencer(Comando):
    """Comando para actualizar el perfil de un influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 descripcion: Optional[str] = None,
                 biografia: Optional[str] = None,
                 sitio_web: Optional[str] = None):
        super().__init__()
        self.influencer_id = influencer_id
        self.descripcion = descripcion
        self.biografia = biografia
        self.sitio_web = sitio_web
