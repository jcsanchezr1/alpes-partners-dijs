"""Versión simplificada del comando RegistrarInfluencer para debugging."""

from typing import Optional, List
from dataclasses import dataclass
import logging

# Importaciones mínimas y directas
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, '..', '..', '..', '..', '..')
src_path = os.path.normpath(src_path)
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from alpes_partners.seedwork.aplicacion.comandos import Comando
from alpes_partners.seedwork.aplicacion.comandos import ejecutar_commando as comando

logger = logging.getLogger(__name__)

@dataclass
class RegistrarInfluencerSimple(Comando):
    """Comando simplificado para registrar un influencer."""
    fecha_creacion: str
    fecha_actualizacion: str
    id: str
    nombre: str
    email: str
    categorias: List[str]
    descripcion: Optional[str] = None
    biografia: Optional[str] = None
    sitio_web: Optional[str] = None
    telefono: Optional[str] = None


@comando.register(RegistrarInfluencerSimple)
def ejecutar_comando_registrar_influencer_simple(comando: RegistrarInfluencerSimple):
    """Ejecutor simplificado del comando."""
    logger.info(f"🎯 EJECUTOR SIMPLE: Procesando comando - ID: {comando.id}")
    logger.info(f"🎯 EJECUTOR SIMPLE: Nombre: {comando.nombre}, Email: {comando.email}")
    # Por ahora solo loggeamos, sin crear entidades
    logger.info(f"✅ EJECUTOR SIMPLE: Comando procesado exitosamente")

# Log para confirmar que el módulo se carga
logger.info("🔧 MÓDULO SIMPLE: registrar_influencer_simple.py cargado y comando registrado")
