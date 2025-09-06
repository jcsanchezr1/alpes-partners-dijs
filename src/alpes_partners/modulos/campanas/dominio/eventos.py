from datetime import datetime
from typing import List, Dict, Any
from alpes_partners.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from .objetos_valor import TipoComision, EstadoCampana


class CampanaCreada(EventoIntegracion):
    """Evento emitido cuando se crea una nueva campana."""
    
    def __init__(self, 
                 campana_id: str,
                 nombre: str,
                 descripcion: str,
                 tipo_comision: TipoComision,
                 valor_comision: float,
                 moneda: str,
                 categorias_objetivo: List[str],
                 fecha_inicio: datetime,
                 fecha_fin: datetime = None):
        super().__init__()
        self.campana_id = campana_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.tipo_comision = tipo_comision
        self.valor_comision = valor_comision
        self.moneda = moneda
        self.categorias_objetivo = categorias_objetivo
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'tipo_comision': self.tipo_comision.value,
            'valor_comision': self.valor_comision,
            'moneda': self.moneda,
            'categorias_objetivo': self.categorias_objetivo,
            'fecha_inicio': self.fecha_inicio.isoformat(),
            'fecha_fin': self.fecha_fin.isoformat() if self.fecha_fin else None
        }


class CampanaActivada(EventoIntegracion):
    """Evento emitido cuando se activa una campana."""
    
    def __init__(self, 
                 campana_id: str,
                 nombre: str,
                 fecha_activacion: datetime):
        super().__init__()
        self.campana_id = campana_id
        self.nombre = nombre
        self.fecha_activacion = fecha_activacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'nombre': self.nombre,
            'fecha_activacion': self.fecha_activacion.isoformat()
        }


class AfiliadoAsignadoACampana(EventoIntegracion):
    """Evento emitido cuando se asigna un afiliado a una campana."""
    
    def __init__(self, 
                 campana_id: str,
                 afiliado_id: str,
                 nombre_campana: str,
                 nombre_afiliado: str,
                 fecha_asignacion: datetime):
        super().__init__()
        self.campana_id = campana_id
        self.afiliado_id = afiliado_id
        self.nombre_campana = nombre_campana
        self.nombre_afiliado = nombre_afiliado
        self.fecha_asignacion = fecha_asignacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'afiliado_id': self.afiliado_id,
            'nombre_campana': self.nombre_campana,
            'nombre_afiliado': self.nombre_afiliado,
            'fecha_asignacion': self.fecha_asignacion.isoformat()
        }


class OportunidadCampanaDisponible(EventoIntegracion):
    """Evento emitido cuando hay una oportunidad de campana disponible para un afiliado."""
    
    def __init__(self, 
                 campana_id: str,
                 afiliado_id: str,
                 nombre_campana: str,
                 tipo_comision: TipoComision,
                 valor_comision: float,
                 categorias_compatibles: List[str],
                 fecha_oportunidad: datetime):
        super().__init__()
        self.campana_id = campana_id
        self.afiliado_id = afiliado_id
        self.nombre_campana = nombre_campana
        self.tipo_comision = tipo_comision
        self.valor_comision = valor_comision
        self.categorias_compatibles = categorias_compatibles
        self.fecha_oportunidad = fecha_oportunidad
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'afiliado_id': self.afiliado_id,
            'nombre_campana': self.nombre_campana,
            'tipo_comision': self.tipo_comision.value,
            'valor_comision': self.valor_comision,
            'categorias_compatibles': self.categorias_compatibles,
            'fecha_oportunidad': self.fecha_oportunidad.isoformat()
        }


class CampanaPausada(EventoDominio):
    """Evento emitido cuando se pausa una campana."""
    
    def __init__(self, 
                 campana_id: str,
                 motivo: str,
                 fecha_pausa: datetime):
        super().__init__()
        self.campana_id = campana_id
        self.motivo = motivo
        self.fecha_pausa = fecha_pausa
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'motivo': self.motivo,
            'fecha_pausa': self.fecha_pausa.isoformat()
        }


class TerminosCampanaActualizados(EventoDominio):
    """Evento emitido cuando se actualizan los términos de una campana."""
    
    def __init__(self, 
                 campana_id: str,
                 cambios_realizados: Dict[str, Any],
                 fecha_actualizacion: datetime):
        super().__init__()
        self.campana_id = campana_id
        self.cambios_realizados = cambios_realizados
        self.fecha_actualizacion = fecha_actualizacion
    
    def _datos_evento(self) -> Dict[str, Any]:
        return {
            'campana_id': self.campana_id,
            'cambios_realizados': self.cambios_realizados,
            'fecha_actualizacion': self.fecha_actualizacion.isoformat()
        }
