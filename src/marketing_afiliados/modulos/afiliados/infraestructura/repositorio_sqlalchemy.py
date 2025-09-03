from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_
import logging

from ..dominio.repositorios import RepositorioAfiliados
from ..dominio.entidades import Afiliado
from ..dominio.objetos_valor import TipoAfiliado, EstadoAfiliado
from .modelos import AfiliadoModelo
from .mappers import AfiliadoMapper

logger = logging.getLogger(__name__)


class RepositorioAfiliadosSQLAlchemy(RepositorioAfiliados):
    """Implementación del repositorio de afiliados con SQLAlchemy síncrono."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def obtener_por_id(self, id: str) -> Optional[Afiliado]:
        """Obtiene un afiliado por su ID."""
        modelo = self.session.query(AfiliadoModelo).filter(AfiliadoModelo.id == id).first()
        
        if modelo:
            return AfiliadoMapper.a_entidad(modelo)
        return None
    
    def agregar(self, entidad: Afiliado) -> None:
        """Agrega un nuevo afiliado."""
        logger.info(f"🔄 REPOSITORIO: Agregando afiliado - ID: {entidad.id}, Email: {entidad.email.valor}")
        
        modelo = AfiliadoMapper.a_modelo(entidad)
        logger.info(f"🔄 REPOSITORIO: Modelo SQLAlchemy creado - ID: {modelo.id}")
        
        self.session.add(modelo)
        logger.info(f"✅ REPOSITORIO: Afiliado agregado a la sesión - ID: {modelo.id}")
        
        # Verificar que esté en la sesión
        if modelo in self.session.new:
            logger.info(f"✅ REPOSITORIO: Confirmado - El modelo está en session.new")
        else:
            logger.warning(f"⚠️ REPOSITORIO: PROBLEMA - El modelo NO está en session.new")
        
        # El commit se hace en la UoW
    
    def actualizar(self, entidad: Afiliado) -> None:
        """Actualiza un afiliado existente."""
        modelo = self.session.query(AfiliadoModelo).filter(AfiliadoModelo.id == entidad.id).first()
        
        if modelo:
            AfiliadoMapper.actualizar_modelo(modelo, entidad)
            # El commit se hace en la UoW
    
    def eliminar(self, entidad: Afiliado) -> None:
        """Elimina un afiliado."""
        modelo = self.session.query(AfiliadoModelo).filter(AfiliadoModelo.id == entidad.id).first()
        
        if modelo:
            self.session.delete(modelo)
            # El commit se hace en la UoW
    
    def obtener_todos(self) -> List[Afiliado]:
        """Obtiene todos los afiliados."""
        modelos = self.session.query(AfiliadoModelo).order_by(AfiliadoModelo.fecha_creacion.desc()).all()
        
        return [AfiliadoMapper.a_entidad(modelo) for modelo in modelos]
    
    def obtener_por_email(self, email: str) -> Optional[Afiliado]:
        """Obtiene un afiliado por su email."""
        modelo = self.session.query(AfiliadoModelo).filter(AfiliadoModelo.email == email).first()
        
        if modelo:
            return AfiliadoMapper.a_entidad(modelo)
        return None
    
    def obtener_por_estado(self, estado: EstadoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por estado."""
        modelos = self.session.query(AfiliadoModelo).filter(
            AfiliadoModelo.estado == estado
        ).order_by(AfiliadoModelo.fecha_creacion.desc()).all()
        
        return [AfiliadoMapper.a_entidad(modelo) for modelo in modelos]
    
    def obtener_por_tipo(self, tipo: TipoAfiliado) -> List[Afiliado]:
        """Obtiene afiliados por tipo."""
        modelos = self.session.query(AfiliadoModelo).filter(
            AfiliadoModelo.tipo_afiliado == tipo
        ).order_by(AfiliadoModelo.fecha_creacion.desc()).all()
        
        return [AfiliadoMapper.a_entidad(modelo) for modelo in modelos]
    
    def obtener_por_categoria(self, categoria: str) -> List[Afiliado]:
        """Obtiene afiliados que manejan una categoría específica."""
        # Usamos el operador JSON para buscar en el array de categorías
        modelos = self.session.query(AfiliadoModelo).filter(
            AfiliadoModelo.categorias.op('@>')([categoria.lower()])
        ).order_by(AfiliadoModelo.fecha_creacion.desc()).all()
        
        return [AfiliadoMapper.a_entidad(modelo) for modelo in modelos]
    
    def buscar_por_nombre(self, nombre: str) -> List[Afiliado]:
        """Busca afiliados por nombre (búsqueda parcial)."""
        modelos = self.session.query(AfiliadoModelo).filter(
            AfiliadoModelo.nombre.ilike(f"%{nombre}%")
        ).order_by(AfiliadoModelo.fecha_creacion.desc()).all()
        
        return [AfiliadoMapper.a_entidad(modelo) for modelo in modelos]
    
    def existe_email(self, email: str) -> bool:
        """Verifica si existe un afiliado con el email dado."""
        return self.session.query(AfiliadoModelo.id).filter(AfiliadoModelo.email == email).first() is not None
