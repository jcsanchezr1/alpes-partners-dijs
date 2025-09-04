from datetime import datetime
from typing import Optional, Dict, List
from ....seedwork.dominio.entidades import AgregacionRaiz
from ....seedwork.dominio.objetos_valor import Email, Telefono
from ....seedwork.dominio.excepciones import ExcepcionReglaDeNegocio, ExcepcionEstadoInvalido
from .objetos_valor import (
    TipoInfluencer, EstadoInfluencer, PerfilInfluencer, 
    MetricasInfluencer, CategoriaInfluencer, DatosAudiencia,
    Demografia, Plataforma
)
from .eventos import (
    InfluencerRegistrado, InfluencerActivado, InfluencerDesactivado,
    PerfilInfluencerActualizado, AudienciaInfluencerActualizada,
    MetricasInfluencerActualizadas
)
from .excepciones import PlataformaNoSoportada, DatosAudienciaInvalidos


class Influencer(AgregacionRaiz):
    """Agregado raíz para Influencer."""
    
    def __init__(self, 
                 nombre: str,
                 email: Email,
                 perfil: PerfilInfluencer,
                 telefono: Optional[Telefono] = None,
                 id: Optional[str] = None):
        super().__init__(id)
        self.nombre = nombre.strip()
        self.email = email
        self.telefono = telefono
        self.perfil = perfil
        self.estado = EstadoInfluencer.PENDIENTE
        self.metricas = MetricasInfluencer()
        self.audiencia_por_plataforma: Dict[Plataforma, DatosAudiencia] = {}
        self.demografia: Optional[Demografia] = None
        self.fecha_activacion: Optional[datetime] = None
        self.fecha_desactivacion: Optional[datetime] = None
        
        # Validaciones
        if not self.nombre:
            raise ExcepcionReglaDeNegocio("El nombre del influencer es requerido")
        
        # Emitir evento de registro
        self.agregar_evento(InfluencerRegistrado(
            influencer_id=self.id,
            nombre=self.nombre,
            email=self.email.valor,
            categorias=self.perfil.categorias.categorias,
            plataformas=[],  # Se actualizará cuando se agreguen plataformas
            fecha_registro=self.fecha_creacion
        ))
    
    @classmethod
    def crear(cls, 
              nombre: str,
              email: str,
              categorias: list,
              descripcion: str,
              biografia: str = "",
              sitio_web: str = "",
              telefono: str = "") -> 'Influencer':
        """Factory method para crear un influencer."""
        
        email_obj = Email(email)
        telefono_obj = Telefono(telefono) if telefono else None
        categoria_obj = CategoriaInfluencer(categorias)
        
        perfil = PerfilInfluencer(
            categorias=categoria_obj,
            descripcion=descripcion,
            biografia=biografia,
            sitio_web=sitio_web
        )
        
        return cls(
            nombre=nombre,
            email=email_obj,
            perfil=perfil,
            telefono=telefono_obj
        )
    
    def crear_influencer(self, influencer: 'Influencer') -> None:
        """Método para procesar la creación del influencer (similar a crear_reserva)."""
        # Este método puede contener lógica adicional de validación o procesamiento
        # Por ahora, simplemente valida que el influencer esté en estado correcto
        if self.estado != EstadoInfluencer.PENDIENTE:
            raise ExcepcionEstadoInvalido("El influencer debe estar en estado PENDIENTE para ser procesado")
        
        # Importar el evento aquí para evitar imports circulares
        from .eventos import InfluencerRegistrado
        
        # Emitir evento de influencer registrado
        self.agregar_evento(InfluencerRegistrado(
            influencer_id=str(self.id),
            nombre=self.nombre,  # nombre es str, no objeto valor
            email=self.email.valor,  # email es objeto valor
            categorias=self.perfil.categorias.categorias if hasattr(self.perfil, 'categorias') else [],
            plataformas=[p.valor for p in self.plataformas] if hasattr(self, 'plataformas') and self.plataformas else [],
            fecha_registro=self.fecha_creacion
        ))
    
    def activar(self) -> None:
        """Activa el influencer."""
        if self.estado == EstadoInfluencer.ACTIVO:
            raise ExcepcionEstadoInvalido("El influencer ya está activo")
        
        if self.estado == EstadoInfluencer.SUSPENDIDO:
            raise ExcepcionEstadoInvalido("No se puede activar un influencer suspendido")
        
        self.estado = EstadoInfluencer.ACTIVO
        self.fecha_activacion = datetime.utcnow()
        
        # Importar el evento aquí para evitar imports circulares
        from .eventos import InfluencerActivado
        
        # Emitir evento de influencer activado
        self.agregar_evento(InfluencerActivado(
            influencer_id=str(self.id),
            nombre=self.nombre,  # nombre es str, no objeto valor
            plataformas=[p.valor for p in self.plataformas] if hasattr(self, 'plataformas') and self.plataformas else [],
            fecha_activacion=self.fecha_activacion
        ))
    
    def desactivar(self, motivo: str) -> None:
        """Desactiva el influencer."""
        if self.estado == EstadoInfluencer.INACTIVO:
            raise ExcepcionEstadoInvalido("El influencer ya está inactivo")
        
        if not motivo.strip():
            raise ExcepcionReglaDeNegocio("El motivo de desactivación es requerido")
        
        self.estado = EstadoInfluencer.INACTIVO
        self.fecha_desactivacion = datetime.utcnow()
        
        # Importar el evento aquí para evitar imports circulares
        from .eventos import InfluencerDesactivado
        
        # Emitir evento de influencer desactivado
        self.agregar_evento(InfluencerDesactivado(
            influencer_id=str(self.id),
            nombre=self.nombre,  # nombre es str, no objeto valor
            motivo=motivo,
            fecha_desactivacion=self.fecha_desactivacion
        ))
    
    def suspender(self, motivo: str) -> None:
        """Suspende el influencer."""
        if self.estado == EstadoInfluencer.SUSPENDIDO:
            raise ExcepcionEstadoInvalido("El influencer ya está suspendido")
        
        if not motivo.strip():
            raise ExcepcionReglaDeNegocio("El motivo de suspensión es requerido")
        
        self.estado = EstadoInfluencer.SUSPENDIDO
        self.incrementar_version()
    
    def actualizar_perfil(self, 
                         descripcion: Optional[str] = None,
                         biografia: Optional[str] = None,
                         sitio_web: Optional[str] = None) -> None:
        """Actualiza el perfil del influencer."""
        cambios = {}
        
        if descripcion is not None and descripcion.strip():
            cambios['descripcion'] = descripcion.strip()
        
        if biografia is not None:
            cambios['biografia'] = biografia.strip()
        
        if sitio_web is not None:
            cambios['sitio_web'] = sitio_web.strip()
        
        if cambios:
            # Crear nuevo perfil con los cambios
            nuevo_perfil = PerfilInfluencer(
                categorias=self.perfil.categorias,
                descripcion=cambios.get('descripcion', self.perfil.descripcion),
                biografia=cambios.get('biografia', self.perfil.biografia),
                sitio_web=cambios.get('sitio_web', self.perfil.sitio_web)
            )
            
            self.perfil = nuevo_perfil
            self.incrementar_version()
            
            # Emitir evento
            self.agregar_evento(PerfilInfluencerActualizado(
                influencer_id=self.id,
                cambios_realizados=cambios,
                fecha_actualizacion=datetime.utcnow()
            ))
    
    def agregar_plataforma(self, datos_audiencia: DatosAudiencia) -> None:
        """Agrega o actualiza datos de audiencia para una plataforma."""
        if datos_audiencia.plataforma in self.audiencia_por_plataforma:
            # Actualizar datos existentes
            datos_anteriores = self.audiencia_por_plataforma[datos_audiencia.plataforma]
            if datos_audiencia.seguidores < datos_anteriores.seguidores:
                raise DatosAudienciaInvalidos("Los nuevos seguidores no pueden ser menores a los anteriores")
        
        self.audiencia_por_plataforma[datos_audiencia.plataforma] = datos_audiencia
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(AudienciaInfluencerActualizada(
            influencer_id=self.id,
            plataforma=datos_audiencia.plataforma.value,
            nuevos_seguidores=datos_audiencia.seguidores,
            nuevo_engagement=datos_audiencia.engagement_rate,
            fecha_actualizacion=datetime.utcnow()
        ))
    
    def actualizar_demografia(self, demografia: Demografia) -> None:
        """Actualiza la demografía del influencer."""
        self.demografia = demografia
        self.incrementar_version()
    
    def actualizar_metricas(self, 
                           campañas_completadas: int = 0,
                           engagement_promedio: float = 0.0,
                           cpm_promedio: float = 0.0,
                           ingresos: float = 0.0) -> None:
        """Actualiza las métricas del influencer."""
        nueva_metricas = MetricasInfluencer(
            campañas_completadas=self.metricas.campañas_completadas + campañas_completadas,
            engagement_promedio=engagement_promedio if engagement_promedio > 0 else self.metricas.engagement_promedio,
            cpm_promedio=cpm_promedio if cpm_promedio > 0 else self.metricas.cpm_promedio,
            ingresos_generados=self.metricas.ingresos_generados + ingresos
        )
        
        self.metricas = nueva_metricas
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(MetricasInfluencerActualizadas(
            influencer_id=self.id,
            campañas_completadas=nueva_metricas.campañas_completadas,
            ingresos_generados=nueva_metricas.ingresos_generados,
            fecha_actualizacion=datetime.utcnow()
        ))
    
    def puede_participar_en_campañas(self) -> bool:
        """Verifica si el influencer puede participar en campañas."""
        return (self.estado == EstadoInfluencer.ACTIVO and 
                len(self.audiencia_por_plataforma) > 0)
    
    def es_compatible_con_categoria(self, categoria: str) -> bool:
        """Verifica si el influencer maneja una categoría específica."""
        return categoria.lower() in self.perfil.categorias.categorias
    
    def obtener_tipo_principal(self) -> Optional[TipoInfluencer]:
        """Obtiene el tipo de influencer basado en la plataforma con más seguidores."""
        if not self.audiencia_por_plataforma:
            return None
        
        plataforma_principal = max(
            self.audiencia_por_plataforma.values(),
            key=lambda x: x.seguidores
        )
        
        return plataforma_principal.calcular_tipo_influencer()
    
    def obtener_engagement_promedio(self) -> float:
        """Calcula el engagement promedio across todas las plataformas."""
        if not self.audiencia_por_plataforma:
            return 0.0
        
        total_engagement = sum(datos.engagement_rate for datos in self.audiencia_por_plataforma.values())
        return total_engagement / len(self.audiencia_por_plataforma)
    
    def obtener_total_seguidores(self) -> int:
        """Obtiene el total de seguidores across todas las plataformas."""
        return sum(datos.seguidores for datos in self.audiencia_por_plataforma.values())
