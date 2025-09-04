import pulsar
from pulsar.schema import *

from alpes_partners.modulos.influencers.infraestructura.schema.v1.eventos import (
    EventoInfluencerRegistrado, InfluencerRegistradoPayload,
    EventoInfluencerActivado, InfluencerActivadoPayload,
    EventoInfluencerDesactivado, InfluencerDesactivadoPayload
)
from alpes_partners.modulos.influencers.infraestructura.schema.v1.comandos import (
    ComandoRegistrarInfluencer, RegistrarInfluencerPayload
)
from alpes_partners.seedwork.infraestructura import utils

import datetime

epoch = datetime.datetime.utcfromtimestamp(0)

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0


class DespachadorInfluencers:
    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()

    def publicar_evento_influencer_registrado(self, evento, topico='eventos-influencers'):
        """Publica evento cuando un influencer es registrado."""
        payload = InfluencerRegistradoPayload(
            id_influencer=str(evento.influencer_id), 
            nombre=str(evento.nombre), 
            email=str(evento.email), 
            categorias=evento.categorias,
            fecha_registro=int(unix_time_millis(evento.fecha_registro))
        )
        evento_integracion = EventoInfluencerRegistrado(
            id=str(evento.id),
            time=int(unix_time_millis(evento.fecha_registro)),
            ingestion=int(unix_time_millis(datetime.datetime.utcnow())),
            specversion="1.0",
            type="InfluencerRegistrado",
            datacontenttype="application/json",
            service_name="alpes-partners-influencers",
            data=payload
        )
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoInfluencerRegistrado))

    def publicar_evento_influencer_activado(self, evento, topico='eventos-influencers'):
        """Publica evento cuando un influencer es activado."""
        payload = InfluencerActivadoPayload(
            id_influencer=str(evento.influencer_id), 
            nombre=str(evento.nombre), 
            email="",  # El evento InfluencerActivado no tiene email, usar vacío
            fecha_activacion=int(unix_time_millis(evento.fecha_activacion))
        )
        evento_integracion = EventoInfluencerActivado(
            id=str(evento.id),
            time=int(unix_time_millis(evento.fecha_activacion)),
            ingestion=int(unix_time_millis(datetime.datetime.utcnow())),
            specversion="1.0",
            type="InfluencerActivado",
            datacontenttype="application/json",
            service_name="alpes-partners-influencers",
            data=payload
        )
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoInfluencerActivado))

    def publicar_evento_influencer_desactivado(self, evento, topico='eventos-influencers'):
        """Publica evento cuando un influencer es desactivado."""
        payload = InfluencerDesactivadoPayload(
            id_influencer=str(evento.influencer_id), 
            nombre=str(evento.nombre), 
            email="",  # El evento InfluencerDesactivado no tiene email, usar vacío
            motivo=str(evento.motivo),
            fecha_desactivacion=int(unix_time_millis(evento.fecha_desactivacion))
        )
        evento_integracion = EventoInfluencerDesactivado(
            id=str(evento.id),
            time=int(unix_time_millis(evento.fecha_desactivacion)),
            ingestion=int(unix_time_millis(datetime.datetime.utcnow())),
            specversion="1.0",
            type="InfluencerDesactivado",
            datacontenttype="application/json",
            service_name="alpes-partners-influencers",
            data=payload
        )
        self._publicar_mensaje(evento_integracion, topico, AvroSchema(EventoInfluencerDesactivado))

    def publicar_comando_registrar_influencer(self, comando, topico='comandos-influencers'):
        """Publica comando para registrar influencer."""
        payload = RegistrarInfluencerPayload(
            id_usuario=str(comando.id_usuario),
            nombre=str(comando.nombre),
            email=str(comando.email),
            categorias=comando.categorias,
            descripcion=str(comando.descripcion),
            biografia=str(comando.biografia),
            sitio_web=str(comando.sitio_web),
            telefono=str(comando.telefono)
        )
        comando_integracion = ComandoRegistrarInfluencer(
            id=str(comando.id),
            time=int(unix_time_millis(datetime.datetime.utcnow())),
            ingestion=int(unix_time_millis(datetime.datetime.utcnow())),
            specversion="1.0",
            type="RegistrarInfluencer",
            datacontenttype="application/json",
            service_name="alpes-partners-influencers",
            data=payload
        )
        self._publicar_mensaje(comando_integracion, topico, AvroSchema(ComandoRegistrarInfluencer))
