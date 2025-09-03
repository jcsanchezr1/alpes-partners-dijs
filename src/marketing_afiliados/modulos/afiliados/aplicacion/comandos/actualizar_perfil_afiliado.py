from typing import Optional, Dict
from src.marketing_afiliados.seedwork.aplicacion.comandos import Comando


class ActualizarPerfilAfiliado(Comando):
    """Comando para actualizar el perfil de un afiliado."""
    
    def __init__(self, 
                 afiliado_id: str,
                 descripcion: Optional[str] = None,
                 sitio_web: Optional[str] = None,
                 redes_sociales: Optional[Dict[str, str]] = None):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.descripcion = descripcion
        self.sitio_web = sitio_web
        self.redes_sociales = redes_sociales
