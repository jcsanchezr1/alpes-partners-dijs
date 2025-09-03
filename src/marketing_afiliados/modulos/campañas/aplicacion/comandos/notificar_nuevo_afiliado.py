from typing import List
from ....seedwork.aplicacion.comandos import Comando


class NotificarNuevoAfiliado(Comando):
    """Comando para notificar sobre un nuevo afiliado disponible."""
    
    def __init__(self, 
                 afiliado_id: str,
                 nombre: str,
                 tipo_afiliado: str,
                 categorias: List[str]):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.nombre = nombre
        self.tipo_afiliado = tipo_afiliado
        self.categorias = categorias
