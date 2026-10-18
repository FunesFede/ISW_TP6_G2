from datetime import datetime
from typing import List, Optional, Set

from app.dominio.modelos import Inscripcion


class RepositorioInscripcionesEnMemoria:

    def __init__(self):
        self._inscripciones: List[Inscripcion] = []

    def guardar(self, inscripcion: Inscripcion) -> None:
        self._inscripciones.append(inscripcion)

    def dnis_inscriptos_en(self, horario: datetime) -> Set[str]:
        return {
            visitante.dni
            for inscripcion in self._inscripciones
            if inscripcion.horario == horario
            for visitante in inscripcion.visitantes
        }

    def buscar(self, codigo: str) -> Optional[Inscripcion]:
        for inscripcion in self._inscripciones:
            if inscripcion.codigo == codigo:
                return inscripcion
        return None
