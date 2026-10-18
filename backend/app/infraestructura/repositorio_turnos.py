from datetime import date, datetime
from typing import Dict, Iterable, List, Optional, Tuple

from app.dominio.modelos import Turno


class RepositorioTurnosEnMemoria:

    def __init__(self, turnos: Iterable[Turno] = ()):
        self._turnos: Dict[Tuple[str, datetime], Turno] = {}
        for turno in turnos:
            self.guardar(turno)

    def obtener(self, actividad: str, inicio: datetime) -> Optional[Turno]:
        return self._turnos.get((actividad, inicio))

    def guardar(self, turno: Turno) -> None:
        self._turnos[(turno.actividad, turno.inicio)] = turno

    def listar(self, actividad: str, fecha: date) -> List[Turno]:
        return sorted(
            (
                turno for (nombre, inicio), turno in self._turnos.items()
                if nombre == actividad and inicio.date() == fecha
            ),
            key=lambda turno: turno.inicio,
        )
