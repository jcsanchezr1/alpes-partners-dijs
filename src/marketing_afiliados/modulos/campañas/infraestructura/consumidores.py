from typing import Dict, Any, List
from datetime import datetime
from ...seedwork.infraestructura.eventos import ConsumidorEventos
from ..aplicacion.comandos.notificar_nuevo_afiliado import NotificarNuevoAfiliado
from ..dominio.objetos_valor import TipoAfiliado, EstadoCampaña
from ..dominio.eventos import OportunidadCampañaDisponible


class ConsumidorEventosAfiliados:
    """Consumidor de eventos del módulo Afiliados."""
    
    def __init__(self, mediador, repositorio_campañas):
        self.mediador = mediador
        self.repositorio_campañas = repositorio_campañas
    
    async def cuando_afiliado_registrado(self, evento: Dict[str, Any]) -> None:
        """Maneja el evento AfiliadoRegistrado."""
        print(f"Nuevo afiliado registrado: {evento['nombre']}")
        
        # Buscar campañas activas compatibles
        campañas_compatibles = await self._buscar_campañas_compatibles(
            tipo_afiliado=evento['tipo_afiliado'],
            categorias=evento['categorias']
        )
        
        # Generar eventos de oportunidad para cada campaña compatible
        for campaña in campañas_compatibles:
            evento_oportunidad = OportunidadCampañaDisponible(
                campaña_id=campaña.id,
                afiliado_id=evento['afiliado_id'],
                nombre_campaña=campaña.nombre,
                tipo_comision=campaña.terminos_comision.tipo,
                valor_comision=campaña.terminos_comision.valor.cantidad,
                categorias_compatibles=self._obtener_categorias_compatibles(
                    evento['categorias'], 
                    campaña.criterios_afiliado.categorias_requeridas
                ),
                fecha_oportunidad=datetime.utcnow()
            )
            
            # Agregar evento a la campaña
            campaña.agregar_evento(evento_oportunidad)
            await self.repositorio_campañas.actualizar(campaña)
    
    async def cuando_afiliado_activado(self, evento: Dict[str, Any]) -> None:
        """Maneja el evento AfiliadoActivado."""
        print(f"Afiliado activado: {evento['nombre']}")
        
        # Lógica similar a cuando_afiliado_registrado
        # pero para afiliados que se activan después del registro
    
    async def cuando_afiliado_desactivado(self, evento: Dict[str, Any]) -> None:
        """Maneja el evento AfiliadoDesactivado."""
        print(f"Afiliado desactivado: {evento['nombre']}")
        
        # Remover afiliado de campañas activas
        campañas_activas = await self.repositorio_campañas.obtener_por_estado(EstadoCampaña.ACTIVA)
        
        for campaña in campañas_activas:
            if evento['afiliado_id'] in campaña.afiliados_asignados:
                campaña.remover_afiliado(evento['afiliado_id'])
                await self.repositorio_campañas.actualizar(campaña)
    
    async def _buscar_campañas_compatibles(self, tipo_afiliado: str, categorias: List[str]) -> List:
        """Busca campañas compatibles con el afiliado."""
        campañas_activas = await self.repositorio_campañas.obtener_por_estado(EstadoCampaña.ACTIVA)
        
        campañas_compatibles = []
        for campaña in campañas_activas:
            if campaña.puede_asignar_afiliado(categorias, tipo_afiliado):
                campañas_compatibles.append(campaña)
        
        return campañas_compatibles
    
    def _obtener_categorias_compatibles(self, categorias_afiliado: List[str], categorias_campaña: List[str]) -> List[str]:
        """Obtiene las categorías compatibles entre afiliado y campaña."""
        return list(set(categorias_afiliado) & set(categorias_campaña))
