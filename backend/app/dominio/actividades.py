from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class Actividad:
    nombre: str
    cupo_por_turno: int
    requiere_talle: bool = False
    edad_minima: int = 0


CATALOGO_ACTIVIDADES: Dict[str, Actividad] = {
    actividad.nombre: actividad
    for actividad in (
        Actividad(
            nombre="Tirolesa", cupo_por_turno=10, requiere_talle=True,
            edad_minima=8,
        ),
        Actividad(nombre="Safari", cupo_por_turno=8),
        Actividad(
            nombre="Palestra", cupo_por_turno=12, requiere_talle=True,
            edad_minima=12,
        ),
        Actividad(nombre="Jardinería", cupo_por_turno=12),
    )
}


def buscar_actividad(nombre: str) -> Optional[Actividad]:
    return CATALOGO_ACTIVIDADES.get(nombre)
