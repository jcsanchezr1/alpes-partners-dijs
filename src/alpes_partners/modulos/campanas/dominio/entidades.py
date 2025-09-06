from datetime import datetime
from typing import Optional, List, Dict, Any, Set
from alpes_partners.seedwork.dominio.entidades import AgregacionRaiz
from alpes_partners.seedwork.dominio.objetos_valor import Dinero
from alpes_partners.seedwork.dominio.excepciones import ExcepcionReglaDeNegocio, ExcepcionEstadoInvalido
from .objetos_valor import (
    TipoComision, EstadoCampana, TerminosComision, PeriodoCampana,
    MaterialPromocional, CriteriosAfiliado, MetricasCampana
)
from .eventos import (
    CampanaCreada, CampanaActivada, AfiliadoAsignadoACampana,
    CampanaPausada, TerminosCampanaActualizados
)


class Campana(AgregacionRaiz):
    """Agregado raíz para Campana."""
    
    def __init__(self, 
                 nombre: str,
                 descripcion: str,
                 terminos_comision: TerminosComision,
                 periodo: PeriodoCampana,
                 material_promocional: MaterialPromocional,
                 criterios_afiliado: CriteriosAfiliado,
                 id: Optional[str] = None):
        super().__init__(id)
        self.nombre = nombre.strip()
        self.descripcion = descripcion.strip()
        self.terminos_comision = terminos_comision
        self.periodo = periodo
        self.material_promocional = material_promocional
        self.criterios_afiliado = criterios_afiliado
        self.estado = EstadoCampana.BORRADOR
        self.metricas = MetricasCampana()
        self.afiliados_asignados: Set[str] = set()
        self.fecha_activacion: Optional[datetime] = None
        self.fecha_pausa: Optional[datetime] = None
        
        # Validaciones
        if not self.nombre:
            raise ExcepcionReglaDeNegocio("El nombre de la campana es requerido")
        
        if not self.descripcion:
            raise ExcepcionReglaDeNegocio("La descripción de la campana es requerida")
        
        # Emitir evento de creación
        self.agregar_evento(CampanaCreada(
            campana_id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            tipo_comision=self.terminos_comision.tipo,
            valor_comision=self.terminos_comision.valor.cantidad,
            moneda=self.terminos_comision.valor.moneda,
            categorias_objetivo=self.criterios_afiliado.categorias_requeridas,
            fecha_inicio=self.periodo.fecha_inicio,
            fecha_fin=self.periodo.fecha_fin
        ))
    
    @classmethod
    def crear(cls, 
              nombre: str,
              descripcion: str,
              tipo_comision: TipoComision,
              valor_comision: float,
              moneda: str,
              fecha_inicio: datetime,
              fecha_fin: Optional[datetime] = None,
              titulo_material: str = "",
              descripcion_material: str = "",
              categorias_objetivo: List[str] = None,
              tipos_afiliado_permitidos: List[str] = None) -> 'Campana':
        """Factory method para crear una campana."""
        
        # Crear objetos valor
        dinero_comision = Dinero(valor_comision, moneda)
        terminos = TerminosComision(tipo_comision, dinero_comision)
        periodo = PeriodoCampana(fecha_inicio, fecha_fin)
        
        # Material promocional básico
        material = MaterialPromocional(
            titulo=titulo_material or f"Material para {nombre}",
            descripcion=descripcion_material or descripcion
        )
        
        # Criterios de afiliado
        criterios = CriteriosAfiliado(
            tipos_permitidos=tipos_afiliado_permitidos or [],
            categorias_requeridas=categorias_objetivo or []
        )
        
        return cls(
            nombre=nombre,
            descripcion=descripcion,
            terminos_comision=terminos,
            periodo=periodo,
            material_promocional=material,
            criterios_afiliado=criterios
        )
    
    def activar(self) -> None:
        """Activa la campana."""
        if self.estado == EstadoCampana.ACTIVA:
            raise ExcepcionEstadoInvalido("La campana ya está activa")
        
        if self.estado in [EstadoCampana.FINALIZADA, EstadoCampana.CANCELADA]:
            raise ExcepcionEstadoInvalido("No se puede activar una campana finalizada o cancelada")
        
        # Verificar que esté en período válido
        if not self.periodo.esta_activa():
            raise ExcepcionReglaDeNegocio("No se puede activar una campana fuera de su período de vigencia")
        
        self.estado = EstadoCampana.ACTIVA
        self.fecha_activacion = datetime.utcnow()
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(CampanaActivada(
            campana_id=self.id,
            nombre=self.nombre,
            fecha_activacion=self.fecha_activacion
        ))
    
    def pausar(self, motivo: str) -> None:
        """Pausa la campana."""
        if self.estado != EstadoCampana.ACTIVA:
            raise ExcepcionEstadoInvalido("Solo se pueden pausar campanas activas")
        
        if not motivo.strip():
            raise ExcepcionReglaDeNegocio("El motivo de pausa es requerido")
        
        self.estado = EstadoCampana.PAUSADA
        self.fecha_pausa = datetime.utcnow()
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(CampanaPausada(
            campana_id=self.id,
            motivo=motivo,
            fecha_pausa=self.fecha_pausa
        ))
    
    def reanudar(self) -> None:
        """Reanuda una campana pausada."""
        if self.estado != EstadoCampana.PAUSADA:
            raise ExcepcionEstadoInvalido("Solo se pueden reanudar campanas pausadas")
        
        # Verificar que esté en período válido
        if not self.periodo.esta_activa():
            raise ExcepcionReglaDeNegocio("No se puede reanudar una campana fuera de su período de vigencia")
        
        self.estado = EstadoCampana.ACTIVA
        self.fecha_pausa = None
        self.incrementar_version()
    
    def finalizar(self) -> None:
        """Finaliza la campana."""
        if self.estado == EstadoCampana.FINALIZADA:
            raise ExcepcionEstadoInvalido("La campana ya está finalizada")
        
        if self.estado == EstadoCampana.CANCELADA:
            raise ExcepcionEstadoInvalido("No se puede finalizar una campana cancelada")
        
        self.estado = EstadoCampana.FINALIZADA
        self.incrementar_version()
    
    def asignar_afiliado(self, afiliado_id: str, nombre_afiliado: str) -> None:
        """Asigna un afiliado a la campana."""
        if self.estado != EstadoCampana.ACTIVA:
            raise ExcepcionEstadoInvalido("Solo se pueden asignar afiliados a campanas activas")
        
        if afiliado_id in self.afiliados_asignados:
            raise ExcepcionReglaDeNegocio("El afiliado ya está asignado a esta campana")
        
        self.afiliados_asignados.add(afiliado_id)
        
        # Actualizar métricas
        nueva_metricas = MetricasCampana(
            afiliados_asignados=len(self.afiliados_asignados),
            clics_totales=self.metricas.clics_totales,
            conversiones_totales=self.metricas.conversiones_totales,
            inversion_total=self.metricas.inversion_total,
            ingresos_generados=self.metricas.ingresos_generados
        )
        self.metricas = nueva_metricas
        self.incrementar_version()
        
        # Emitir evento
        self.agregar_evento(AfiliadoAsignadoACampana(
            campana_id=self.id,
            afiliado_id=afiliado_id,
            nombre_campana=self.nombre,
            nombre_afiliado=nombre_afiliado,
            fecha_asignacion=datetime.utcnow()
        ))
    
    def remover_afiliado(self, afiliado_id: str) -> None:
        """Remueve un afiliado de la campana."""
        if afiliado_id not in self.afiliados_asignados:
            raise ExcepcionReglaDeNegocio("El afiliado no está asignado a esta campana")
        
        self.afiliados_asignados.remove(afiliado_id)
        
        # Actualizar métricas
        nueva_metricas = MetricasCampana(
            afiliados_asignados=len(self.afiliados_asignados),
            clics_totales=self.metricas.clics_totales,
            conversiones_totales=self.metricas.conversiones_totales,
            inversion_total=self.metricas.inversion_total,
            ingresos_generados=self.metricas.ingresos_generados
        )
        self.metricas = nueva_metricas
        self.incrementar_version()
    
    def actualizar_terminos(self, 
                           nuevo_valor_comision: Optional[float] = None,
                           nueva_descripcion_comision: Optional[str] = None) -> None:
        """Actualiza los términos de comisión."""
        if self.estado == EstadoCampana.FINALIZADA:
            raise ExcepcionEstadoInvalido("No se pueden actualizar términos de una campana finalizada")
        
        cambios = {}
        
        if nuevo_valor_comision is not None and nuevo_valor_comision > 0:
            nuevo_dinero = Dinero(nuevo_valor_comision, self.terminos_comision.valor.moneda)
            nuevos_terminos = TerminosComision(
                self.terminos_comision.tipo,
                nuevo_dinero,
                nueva_descripcion_comision or self.terminos_comision.descripcion
            )
            self.terminos_comision = nuevos_terminos
            cambios['valor_comision'] = nuevo_valor_comision
        
        if nueva_descripcion_comision is not None:
            cambios['descripcion_comision'] = nueva_descripcion_comision
        
        if cambios:
            self.incrementar_version()
            
            # Emitir evento
            self.agregar_evento(TerminosCampanaActualizados(
                campana_id=self.id,
                cambios_realizados=cambios,
                fecha_actualizacion=datetime.utcnow()
            ))
    
    def puede_asignar_afiliado(self, categorias_afiliado: List[str], tipo_afiliado: str) -> bool:
        """Verifica si un afiliado puede ser asignado a esta campana."""
        if self.estado != EstadoCampana.ACTIVA:
            return False
        
        # Verificar tipos permitidos
        if self.criterios_afiliado.tipos_permitidos:
            if tipo_afiliado not in self.criterios_afiliado.tipos_permitidos:
                return False
        
        # Verificar categorías compatibles
        if self.criterios_afiliado.categorias_requeridas:
            categorias_compatibles = set(categorias_afiliado) & set(self.criterios_afiliado.categorias_requeridas)
            if not categorias_compatibles:
                return False
        
        return True
    
    def actualizar_metricas(self, 
                           clics: int = 0,
                           conversiones: int = 0,
                           inversion: float = 0.0,
                           ingresos: float = 0.0) -> None:
        """Actualiza las métricas de la campana."""
        nueva_metricas = MetricasCampana(
            afiliados_asignados=self.metricas.afiliados_asignados,
            clics_totales=self.metricas.clics_totales + clics,
            conversiones_totales=self.metricas.conversiones_totales + conversiones,
            inversion_total=self.metricas.inversion_total + inversion,
            ingresos_generados=self.metricas.ingresos_generados + ingresos
        )
        
        self.metricas = nueva_metricas
        self.incrementar_version()
    
    def crear_campana(self, campana: 'Campana') -> None:
        """Método para crear la campana y emitir el evento correspondiente."""
        # Emitir evento de creación
        from .eventos import CampanaCreada
        self.agregar_evento(CampanaCreada(
            campana_id=self.id,
            nombre=self.nombre,
            descripcion=self.descripcion,
            tipo_comision=self.terminos_comision.tipo,
            valor_comision=self.terminos_comision.valor.cantidad,
            moneda=self.terminos_comision.valor.moneda,
            categorias_objetivo=self.criterios_afiliado.categorias_requeridas,
            fecha_inicio=self.periodo.fecha_inicio,
            fecha_fin=self.periodo.fecha_fin
        ))
