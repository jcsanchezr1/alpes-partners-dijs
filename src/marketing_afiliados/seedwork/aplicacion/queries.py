from abc import ABC
from datetime import datetime
from typing import Any, Dict, Optional
import uuid


class Query(ABC):
    """Clase base para queries."""
    
    def __init__(self) -> None:
        self.id = str(uuid.uuid4())
        self.fecha_creacion = datetime.utcnow()


class ResultadoQuery:
    """Resultado de una query."""
    
    def __init__(self, datos: Any, exitoso: bool = True, mensaje: Optional[str] = None) -> None:
        self.datos = datos
        self.exitoso = exitoso
        self.mensaje = mensaje
