from datetime import datetime
from typing import List, Dict, Any
from ...seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from .objetos_valor import TipoAfiliado, EstadoAfiliado


class AfiliadoRegistrado(EventoIntegracion):
    """Evento emitido cuando se registra un nuevo afiliado."""
    
    def __init__(self, 
                 afiliado_id: str,
                 nombre: str,
                 email: str,
                 tipo_afiliado: TipoAfiliado,
                 categorias: List[str],
                 fecha_registro: datetime):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.nombre = nombre
        self.email = email
        self.tipo_afiliado = tipo_afiliado
        self.categorias = categorias
        self.fecha_registro = fecha_registro
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'afiliado_id': self.afiliado_id,
            'nombre': self.nombre,
            'email': self.email,
            'tipo_afiliado': self.tipo_afiliado.value,
            'categorias': self.categorias,
            'fecha_registro': self.fecha_registro.isoformat()
        }


class AfiliadoActivado(EventoIntegracion):
    """Evento emitido cuando se activa un afiliado."""
    
    def __init__(self, 
                 afiliado_id: str,
                 nombre: str,
                 tipo_afiliado: TipoAfiliado,
                 fecha_activacion: datetime):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.nombre = nombre
        self.tipo_afiliado = tipo_afiliado
        self.fecha_activacion = fecha_activacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'afiliado_id': self.afiliado_id,
            'nombre': self.nombre,
            'tipo_afiliado': self.tipo_afiliado.value,
            'fecha_activacion': self.fecha_activacion.isoformat()
        }


class AfiliadoDesactivado(EventoIntegracion):
    """Evento emitido cuando se desactiva un afiliado."""
    
    def __init__(self, 
                 afiliado_id: str,
                 nombre: str,
                 motivo: str,
                 fecha_desactivacion: datetime):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.nombre = nombre
        self.motivo = motivo
        self.fecha_desactivacion = fecha_desactivacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'afiliado_id': self.afiliado_id,
            'nombre': self.nombre,
            'motivo': self.motivo,
            'fecha_desactivacion': self.fecha_desactivacion.isoformat()
        }


class PerfilAfiliadoActualizado(EventoDominio):
    """Evento emitido cuando se actualiza el perfil de un afiliado."""
    
    def __init__(self, 
                 afiliado_id: str,
                 cambios_realizados: Dict[str, Any],
                 fecha_actualizacion: datetime):
        super().__init__()
        self.afiliado_id = afiliado_id
        self.cambios_realizados = cambios_realizados
        self.fecha_actualizacion = fecha_actualizacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'afiliado_id': self.afiliado_id,
            'cambios_realizados': self.cambios_realizados,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
