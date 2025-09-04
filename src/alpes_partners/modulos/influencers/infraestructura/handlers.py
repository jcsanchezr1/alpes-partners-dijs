"""
Handlers de integración para eventos de influencers.
Estos handlers se ejecutan después del commit de la transacción
y publican eventos a Apache Pulsar.
"""

from pydispatch import dispatcher

from alpes_partners.modulos.influencers.infraestructura.despachadores import DespachadorInfluencers
from alpes_partners.modulos.influencers.dominio.eventos import (
    InfluencerRegistrado,
    InfluencerActivado, 
    InfluencerDesactivado
)

import logging

logger = logging.getLogger(__name__)


class HandlersIntegracionInfluencers:
    """Handlers para eventos de integración de influencers."""
    
    def __init__(self):
        self.despachador = DespachadorInfluencers()

    def handle_influencer_registrado_integracion(self, sender, **kwargs):
        """Handler para evento InfluencerRegistrado de integración."""
        evento = kwargs.get('evento')
        if evento:
            logger.info(f"📡 PULSAR: Publicando evento InfluencerRegistrado - ID: {evento.influencer_id}")
            try:
                self.despachador.publicar_evento_influencer_registrado(evento)
                logger.info(f"✅ PULSAR: Evento InfluencerRegistrado publicado exitosamente")
            except Exception as e:
                logger.error(f"❌ PULSAR: Error publicando evento InfluencerRegistrado: {e}")
                # En un entorno de producción, aquí podrías implementar retry logic
                # o enviar a una cola de dead letters

    def handle_influencer_activado_integracion(self, sender, **kwargs):
        """Handler para evento InfluencerActivado de integración."""
        evento = kwargs.get('evento')
        if evento:
            logger.info(f"📡 PULSAR: Publicando evento InfluencerActivado - ID: {evento.influencer_id}")
            try:
                self.despachador.publicar_evento_influencer_activado(evento)
                logger.info(f"✅ PULSAR: Evento InfluencerActivado publicado exitosamente")
            except Exception as e:
                logger.error(f"❌ PULSAR: Error publicando evento InfluencerActivado: {e}")

    def handle_influencer_desactivado_integracion(self, sender, **kwargs):
        """Handler para evento InfluencerDesactivado de integración."""
        evento = kwargs.get('evento')
        if evento:
            logger.info(f"📡 PULSAR: Publicando evento InfluencerDesactivado - ID: {evento.influencer_id}")
            try:
                self.despachador.publicar_evento_influencer_desactivado(evento)
                logger.info(f"✅ PULSAR: Evento InfluencerDesactivado publicado exitosamente")
            except Exception as e:
                logger.error(f"❌ PULSAR: Error publicando evento InfluencerDesactivado: {e}")


# Instanciar handlers
handlers_integracion = HandlersIntegracionInfluencers()

# Registrar handlers con pydispatch
dispatcher.connect(
    handlers_integracion.handle_influencer_registrado_integracion,
    signal='InfluencerRegistradoIntegracion',
    sender=dispatcher.Any
)

dispatcher.connect(
    handlers_integracion.handle_influencer_activado_integracion,
    signal='InfluencerActivadoIntegracion',
    sender=dispatcher.Any
)

dispatcher.connect(
    handlers_integracion.handle_influencer_desactivado_integracion,
    signal='InfluencerDesactivadoIntegracion',
    sender=dispatcher.Any
)

logger.info("🔧 HANDLERS: Handlers de integración de Pulsar registrados")
