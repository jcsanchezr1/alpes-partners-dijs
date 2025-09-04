from src.alpes_partners.seedwork.aplicacion.comandos import Comando
from ..dto import DatosAudienciaDTO


class AgregarPlataforma(Comando):
    """Comando para agregar una plataforma a un influencer."""
    
    def __init__(self, influencer_id: str, datos_audiencia: DatosAudienciaDTO):
        super().__init__()
        self.influencer_id = influencer_id
        self.datos_audiencia = datos_audiencia
