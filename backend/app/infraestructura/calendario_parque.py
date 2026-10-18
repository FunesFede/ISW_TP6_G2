from datetime import datetime, time
from typing import AbstractSet, FrozenSet, Tuple

LUNES = 0
DIAS_APERTURA: FrozenSet[int] = frozenset(range(7)) - {LUNES}
HORA_APERTURA = time(8, 30)
HORA_CIERRE = time(19, 0)
# Feriados en que el parque cierra todos los años, como (mes, día).
FERIADOS: FrozenSet[Tuple[int, int]] = frozenset({(12, 25), (1, 1)})


class CalendarioParqueSemanal:
    """Calendario del parque según las respuestas de los PO.

    Abre de martes a domingo de 8:30 a 19 hs y cierra el 25 de
    diciembre y el 1 de enero de cada año.
    """

    def __init__(
        self,
        dias_apertura: AbstractSet[int] = DIAS_APERTURA,
        hora_apertura: time = HORA_APERTURA,
        hora_cierre: time = HORA_CIERRE,
        feriados: AbstractSet[Tuple[int, int]] = FERIADOS,
    ):
        self._dias_apertura = dias_apertura
        self._hora_apertura = hora_apertura
        self._hora_cierre = hora_cierre
        self._feriados = feriados

    def esta_abierto(self, fecha_hora: datetime) -> bool:
        if (fecha_hora.month, fecha_hora.day) in self._feriados:
            return False
        if fecha_hora.weekday() not in self._dias_apertura:
            return False
        return self._hora_apertura <= fecha_hora.time() < self._hora_cierre
