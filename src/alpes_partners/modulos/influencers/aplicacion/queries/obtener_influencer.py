from dataclasses import dataclass
from .....seedwork.aplicacion.queries import Query, QueryHandler, QueryResultado
from .....seedwork.aplicacion.queries import ejecutar_query as query
from ..servicios import ServicioInfluencer
from .....seedwork.infraestructura.uow_sincrono import UnidadDeTrabajoSincrona
from .....seedwork.infraestructura.database import get_db_session
from ...infraestructura.repositorio_sqlalchemy import RepositorioInfluencersSQLAlchemy


@dataclass
class ObtenerInfluencer(Query):
    id: str


@dataclass
class ObtenerInfluencerPorEmail(Query):
    email: str


class ObtenerInfluencerHandler(QueryHandler):
    def handle(self, query: ObtenerInfluencer) -> QueryResultado:
        # Obtener sesión de base de datos
        session_db = next(get_db_session())
        try:
            repositorio = RepositorioInfluencersSQLAlchemy(session_db)
            uow = UnidadDeTrabajoSincrona(session_db)
            servicio = ServicioInfluencer(repositorio, uow)
            
            resultado = servicio.obtener_influencer_por_id(query.id)
            return QueryResultado(resultado=resultado)
        finally:
            session_db.close()


class ObtenerInfluencerPorEmailHandler(QueryHandler):
    def handle(self, query: ObtenerInfluencerPorEmail) -> QueryResultado:
        # Obtener sesión de base de datos
        session_db = next(get_db_session())
        try:
            repositorio = RepositorioInfluencersSQLAlchemy(session_db)
            uow = UnidadDeTrabajoSincrona(session_db)
            servicio = ServicioInfluencer(repositorio, uow)
            
            resultado = servicio.obtener_influencer_por_email(query.email)
            return QueryResultado(resultado=resultado)
        finally:
            session_db.close()


@query.register(ObtenerInfluencer)
def ejecutar_query_obtener_influencer(query: ObtenerInfluencer):
    handler = ObtenerInfluencerHandler()
    return handler.handle(query)


@query.register(ObtenerInfluencerPorEmail)
def ejecutar_query_obtener_influencer_por_email(query: ObtenerInfluencerPorEmail):
    handler = ObtenerInfluencerPorEmailHandler()
    return handler.handle(query)