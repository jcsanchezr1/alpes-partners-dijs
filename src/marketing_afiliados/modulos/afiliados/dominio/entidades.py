from datetime import datetime
from typing import Optional, Dict, Any
from ...seedwork.dominio.entidades import AgregadoRaiz
from ...seedwork.dominio.objetos_valor import Email, Telefono
from ...seedwork.dominio.excepciones import ExcepcionReglaDeNegocio, ExcepcionEstadoInvalido
from .objetos_valor import (
    TipoAfiliado, EstadoAfiliado, PerfilAfiliado, 
    MetricasAfiliado, CategoriaAfiliado
)
from .eventos import (
    AfiliadoRegistrado, AfiliadoActivado, AfiliadoDesactivado,
    PerfilAfiliadoActualizado
)


class Afiliado(AgregadoRaiz):
    """Agregado raíz para Afiliado."""
    
    def __init__(self, 
                 nombre: str,
                 email: Email,
                 perfil: PerfilAfiliado,
                 telefono: Optional[Telefono] = None,
                 id: Optional[str] = None):
        super().__init__(id)
        self.nombre = nombre.strip()
        self.email = email
        self.telefono = telefono
        self.perfil = perfil
        self.estado = EstadoAfiliado.PENDIENTE
        self.metricas = MetricasAfiliado()
        self.fecha_activacion: Optional[datetime] = None
        self.fecha_desactivacion: Optional[datetime] = None
        
        # Validaciones
        if not self.nombre:
            raise ExcepcionReglaDeNegocio("El nombre del afiliado es requerido")
        
        # Emitir evento de registro
        self.agregar_evento(AfiliadoRegistrado(
            afiliado_id=self.id,
            nombre=self.nombre,
            email=self.email.valor,
            tipo_afiliado=self.perfil.tipo,
            categorias=self.perfil.categorias.categorias,
            fecha_registro=self.fecha_creacion
        ))
    
    @classmethod
    def crear(cls, 
              nombre: str,
              email: str,
              tipo_afiliado: TipoAfiliado,
              categorias: list,
              descripcion: str,
              sitio_web: str = "",
              telefono: str = "",
              redes_sociales: dict = None) -> 'Afiliado':
        """Factory method para crear un afiliado."""
        
        email_obj = Email(email)
        telefono_obj = Telefono(telefono) if telefono else None
        categoria_obj = CategoriaAfiliado(categorias)
        
        perfil = PerfilAfiliado(
            tipo=tipo_afiliado,
            categorias=categoria_obj,
            descripcion=descripcion,
            sitio_web=sitio_web,
            redes_sociales=redes_sociales or {}
        )
        
        return cls(
            nombre=nombre,
            email=email_obj,
            perfil=perfil,
            telefono=telefono_obj
        )
    
    def activar(self) -> None:
        """Activa el afiliado."""
        if self.estado == EstadoAfiliado.ACTIVO:
            raise ExcepcionEstadoInvalido("El afiliado ya está activo")
        
        if self.estado == EstadoAfiliado.SUSPENDIDO:
            raise ExcepcionEstadoInvalido("No se puede activar un afiliado suspendido")
        
        self.estado = EstadoAfiliado.ACTIVO
        self.fecha_activacion = datetime.utcnow()
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(AfiliadoActivado(
            afiliado_id=self.id,
            nombre=self.nombre,
            tipo_afiliado=self.perfil.tipo,
            fecha_activacion=self.fecha_activacion
        ))
    
    def desactivar(self, motivo: str) -> None:
        """Desactiva el afiliado."""
        if self.estado == EstadoAfiliado.INACTIVO:
            raise ExcepcionEstadoInvalido("El afiliado ya está inactivo")
        
        if not motivo.strip():
            raise ExcepcionReglaDeNegocio("El motivo de desactivación es requerido")
        
        self.estado = EstadoAfiliado.INACTIVO
        self.fecha_desactivacion = datetime.utcnow()
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(AfiliadoDesactivado(
            afiliado_id=self.id,
            nombre=self.nombre,
            motivo=motivo,
            fecha_desactivacion=self.fecha_desactivacion
        ))
    
    def suspender(self, motivo: str) -> None:
        """Suspende el afiliado."""
        if self.estado == EstadoAfiliado.SUSPENDIDO:
            raise ExcepcionEstadoInvalido("El afiliado ya está suspendido")
        
        if not motivo.strip():
            raise ExcepcionReglaDeNegocio("El motivo de suspensión es requerido")
        
        self.estado = EstadoAfiliado.SUSPENDIDO
        self.incrementar_version()
    
    def actualizar_perfil(self, 
                         descripcion: Optional[str] = None,
                         sitio_web: Optional[str] = None,
                         redes_sociales: Optional[dict] = None) -> None:
        """Actualiza el perfil del afiliado."""
        cambios = {}
        
        if descripcion is not None and descripcion.strip():
            cambios['descripcion'] = descripcion.strip()
        
        if sitio_web is not None:
            cambios['sitio_web'] = sitio_web.strip()
        
        if redes_sociales is not None:
            cambios['redes_sociales'] = redes_sociales
        
        if cambios:
            # Crear nuevo perfil con los cambios
            nuevo_perfil = PerfilAfiliado(
                tipo=self.perfil.tipo,
                categorias=self.perfil.categorias,
                descripcion=cambios.get('descripcion', self.perfil.descripcion),
                sitio_web=cambios.get('sitio_web', self.perfil.sitio_web),
                redes_sociales=cambios.get('redes_sociales', self.perfil.redes_sociales)
            )
            
            self.perfil = nuevo_perfil
            self.incrementar_version()
            
            # Emitir evento
            self.agregar_evento(PerfilAfiliadoActualizado(
                afiliado_id=self.id,
                cambios_realizados=cambios,
                fecha_actualizacion=datetime.utcnow()
            ))
    
    def actualizar_metricas(self, 
                           clics: int = 0,
                           conversiones: int = 0,
                           ingresos: float = 0.0) -> None:
        """Actualiza las métricas del afiliado."""
        nueva_metricas = MetricasAfiliado(
            clics_totales=self.metricas.clics_totales + clics,
            conversiones_totales=self.metricas.conversiones_totales + conversiones,
            ingresos_generados=self.metricas.ingresos_generados + ingresos
        )
        
        self.metricas = nueva_metricas
        self.incrementar_version()
    
    def puede_participar_en_campañas(self) -> bool:
        """Verifica si el afiliado puede participar en campañas."""
        return self.estado == EstadoAfiliado.ACTIVO
    
    def es_compatible_con_categoria(self, categoria: str) -> bool:
        """Verifica si el afiliado maneja una categoría específica."""
        return categoria.lower() in self.perfil.categorias.categorias
