from datetime import datetime
from typing import List, Dict, Any
from ....seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from .objetos_valor import TipoInfluencer, EstadoInfluencer, Plataforma


class InfluencerRegistrado(EventoIntegracion):
    """Evento emitido cuando se registra un nuevo influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 nombre: str,
                 email: str,
                 categorias: List[str],
                 plataformas: List[str],
                 fecha_registro: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.nombre = nombre
        self.email = email
        self.categorias = categorias
        self.plataformas = plataformas
        self.fecha_registro = fecha_registro


class InfluencerActivado(EventoIntegracion):
    """Evento emitido cuando se activa un influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 nombre: str,
                 plataformas: List[str],
                 fecha_activacion: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.nombre = nombre
        self.plataformas = plataformas
        self.fecha_activacion = fecha_activacion


class InfluencerDesactivado(EventoDominio):
    """Evento emitido cuando se desactiva un influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 nombre: str,
                 motivo: str,
                 fecha_desactivacion: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.nombre = nombre
        self.motivo = motivo
        self.fecha_desactivacion = fecha_desactivacion


class PerfilInfluencerActualizado(EventoDominio):
    """Evento emitido cuando se actualiza el perfil de un influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 cambios_realizados: Dict[str, Any],
                 fecha_actualizacion: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.cambios_realizados = cambios_realizados
        self.fecha_actualizacion = fecha_actualizacion


class AudienciaInfluencerActualizada(EventoDominio):
    """Evento emitido cuando se actualizan los datos de audiencia."""
    
    def __init__(self, 
                 influencer_id: str,
                 plataforma: str,
                 nuevos_seguidores: int,
                 nuevo_engagement: float,
                 fecha_actualizacion: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.plataforma = plataforma
        self.nuevos_seguidores = nuevos_seguidores
        self.nuevo_engagement = nuevo_engagement
        self.fecha_actualizacion = fecha_actualizacion


class MetricasInfluencerActualizadas(EventoDominio):
    """Evento emitido cuando se actualizan las métricas del influencer."""
    
    def __init__(self, 
                 influencer_id: str,
                 campanas_completadas: int,
                 ingresos_generados: float,
                 fecha_actualizacion: datetime):
        super().__init__()
        self.influencer_id = influencer_id
        self.campanas_completadas = campanas_completadas
        self.ingresos_generados = ingresos_generados
        self.fecha_actualizacion = fecha_actualizacion
