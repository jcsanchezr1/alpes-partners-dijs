from typing import Optional, Dict, List
from src.marketing_afiliados.seedwork.aplicacion.comandos import Comando
from ..dto import RegistrarAfiliadoDTO


class RegistrarAfiliado(Comando):
    """Comando para registrar un nuevo afiliado."""
    
    def __init__(self, datos: RegistrarAfiliadoDTO):
        super().__init__()
        self.nombre = datos.nombre
        self.email = datos.email
        self.tipo_afiliado = datos.tipo_afiliado
        self.categorias = datos.categorias
        self.descripcion = datos.descripcion
        self.sitio_web = datos.sitio_web
        self.telefono = datos.telefono
        self.redes_sociales = datos.redes_sociales
