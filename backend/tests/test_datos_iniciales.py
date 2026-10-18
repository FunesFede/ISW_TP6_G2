from datetime import date, time

import pytest

from app.infraestructura.calendario_parque import CalendarioParqueSemanal
from app.infraestructura.datos_iniciales import generar_turnos

HORARIOS_ESPERADOS = [time(hora, 0) for hora in range(9, 18)]


def turnos_de(actividad, turnos):
    return [turno for turno in turnos if turno.actividad == actividad]


def test_genera_turnos_solo_en_dias_de_apertura():
    # Del lunes 12 al domingo 18 de octubre de 2026
    turnos = generar_turnos(
        desde=date(2026, 10, 12), dias=7,
        calendario=CalendarioParqueSemanal(),
    )

    dias_con_turnos = {turno.inicio.date() for turno in turnos}
    assert date(2026, 10, 12) not in dias_con_turnos  # lunes
    assert len(dias_con_turnos) == 6


def test_no_genera_turnos_en_feriados():
    turnos = generar_turnos(
        desde=date(2026, 12, 25), dias=1,
        calendario=CalendarioParqueSemanal(),
    )

    assert turnos == []


@pytest.mark.parametrize(
    "actividad", ["Tirolesa", "Safari", "Palestra", "Jardinería"]
)
def test_cada_actividad_tiene_un_turno_por_hora_de_9_a_17(actividad):
    turnos = generar_turnos(
        desde=date(2026, 10, 14), dias=1,
        calendario=CalendarioParqueSemanal(),
    )

    horarios = [turno.inicio.time() for turno in turnos_de(actividad, turnos)]
    assert horarios == HORARIOS_ESPERADOS


@pytest.mark.parametrize(
    "actividad, cupo",
    [("Safari", 8), ("Palestra", 12), ("Jardinería", 12), ("Tirolesa", 10)],
)
def test_cupo_de_cada_turno_segun_la_actividad(actividad, cupo):
    turnos = generar_turnos(
        desde=date(2026, 10, 14), dias=1,
        calendario=CalendarioParqueSemanal(),
    )

    assert all(
        turno.cupo_total == cupo for turno in turnos_de(actividad, turnos)
    )
