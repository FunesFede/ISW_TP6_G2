"""Turnos para correr la aplicación, según las respuestas de los PO."""
from datetime import date, datetime, time, timedelta
from typing import List, Tuple

from app.dominio.actividades import CATALOGO_ACTIVIDADES
from app.dominio.modelos import Turno
from app.dominio.puertos import CalendarioParque

# Un turno por hora de 9 a 18; a las 18 no hay turno.
HORARIOS_TURNOS: Tuple[time, ...] = tuple(
    time(hora, 0) for hora in range(9, 18)
)


def generar_turnos(
    desde: date, dias: int, calendario: CalendarioParque
) -> List[Turno]:
    turnos = []
    for desplazamiento in range(dias):
        dia = desde + timedelta(days=desplazamiento)
        for actividad in CATALOGO_ACTIVIDADES.values():
            for hora in HORARIOS_TURNOS:
                inicio = datetime.combine(dia, hora)
                if calendario.esta_abierto(inicio):
                    turnos.append(Turno(
                        actividad=actividad.nombre,
                        inicio=inicio,
                        cupo_total=actividad.cupo_por_turno,
                    ))
    return turnos
