from datetime import datetime

import pytest

from app.infraestructura.calendario_parque import CalendarioParqueSemanal


@pytest.fixture
def calendario():
    return CalendarioParqueSemanal()


@pytest.mark.parametrize(
    "fecha_hora",
    [
        datetime(2026, 10, 13, 8, 30),   # martes, apertura
        datetime(2026, 10, 14, 15, 30),  # miércoles por la tarde
        datetime(2026, 10, 18, 18, 59),  # domingo, antes del cierre
    ],
)
def test_parque_abierto_de_martes_a_domingo_de_8_30_a_19(
    calendario, fecha_hora
):
    assert calendario.esta_abierto(fecha_hora)


@pytest.mark.parametrize(
    "fecha_hora",
    [
        datetime(2026, 10, 12, 10, 0),  # lunes
        datetime(2026, 10, 14, 8, 29),  # antes de abrir
        datetime(2026, 10, 14, 19, 0),  # a la hora de cierre
        datetime(2026, 10, 14, 21, 0),  # de noche
    ],
)
def test_parque_cerrado_los_lunes_y_fuera_de_horario(calendario, fecha_hora):
    assert not calendario.esta_abierto(fecha_hora)


@pytest.mark.parametrize(
    "fecha_hora",
    [
        datetime(2026, 12, 25, 10, 0),  # viernes de Navidad
        datetime(2027, 1, 1, 10, 0),    # viernes de Año Nuevo
        datetime(2027, 12, 25, 10, 0),  # Navidad del año siguiente
    ],
)
def test_parque_cerrado_el_25_de_diciembre_y_el_1_de_enero_de_cada_anio(
    calendario, fecha_hora
):
    assert not calendario.esta_abierto(fecha_hora)
