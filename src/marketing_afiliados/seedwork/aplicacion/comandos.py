from abc import ABC
from datetime import datetime
from typing import Any, Dict
import uuid


class Comando(ABC):
    """Clase base para comandos."""
    
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.fecha_creacion = datetime.utcnow()


class ComandoIntegracion(Comando):
    """Comandos que cruzan límites de contexto."""
    pass
