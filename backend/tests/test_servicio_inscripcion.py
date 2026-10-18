from datetime import datetime, timedelta

import pytest

from app.dominio.excepciones import (
    ActividadInexistenteError,
    ActividadNoDisponibleError,
    DatosVisitanteInvalidosError,
    EdadInsuficienteError,
    InscripcionCerradaError,
    InscripcionInexistenteError,
    InscripcionNoHabilitadaError,
    ParqueCerradoError,
    SinCupoError,
    TalleRequeridoError,
    TerminosNoAceptadosError,
    VisitanteConInscripcionSuperpuestaError,
)
from app.dominio.modelos import SolicitudInscripcion, Turno, Visitante
from app.infraestructura.repositorio_inscripciones import (
    RepositorioInscripcionesEnMemoria,
)
from app.infraestructura.repositorio_turnos import (
    RepositorioTurnosEnMemoria,
)
from app.servicios.servicio_inscripcion import ServicioInscripcion
from tests.dobles import (
    CalendarioFalso,
    GeneradorQRFalso,
    NotificadorEspia,
    RelojFalso,
)

HORARIO = datetime(2026, 10, 14, 10, 0)


def crear_solicitud(**cambios):
    datos = {
        "actividad": "Safari",
        "horario": HORARIO,
        "visitantes": [Visitante(nombre="Ana", dni="30111222", edad=25)],
        "acepta_terminos": True,
        "email": "ana@mail.com",
    }
    datos.update(cambios)
    return SolicitudInscripcion(**datos)


@pytest.fixture
def repositorio():
    return RepositorioTurnosEnMemoria([
        Turno(actividad="Safari", inicio=HORARIO, cupo_total=10),
        Turno(actividad="Tirolesa", inicio=HORARIO, cupo_total=10),
        Turno(actividad="Jardinería", inicio=HORARIO, cupo_total=10),
        Turno(actividad="Palestra", inicio=HORARIO, cupo_total=10),
    ])


@pytest.fixture
def calendario():
    return CalendarioFalso()


@pytest.fixture
def reloj():
    return RelojFalso(HORARIO - timedelta(hours=2))


@pytest.fixture
def notificador():
    return NotificadorEspia()


@pytest.fixture
def inscripciones():
    return RepositorioInscripcionesEnMemoria()


@pytest.fixture
def servicio(repositorio, calendario, notificador, reloj, inscripciones):
    return ServicioInscripcion(
        repositorio_turnos=repositorio,
        calendario_parque=calendario,
        notificador=notificador,
        generador_qr=GeneradorQRFalso(),
        reloj=reloj,
        repositorio_inscripciones=inscripciones,
    )


def test_inscripcion_valida_devuelve_inscripcion_confirmada(servicio):
    inscripcion = servicio.inscribir(crear_solicitud())

    assert inscripcion.actividad == "Safari"
    assert inscripcion.horario == HORARIO
    assert len(inscripcion.visitantes) == 1


def test_inscripcion_a_actividad_fuera_del_listado_falla(servicio):
    with pytest.raises(ActividadInexistenteError):
        servicio.inscribir(crear_solicitud(actividad="Paracaidismo"))


def test_inscripcion_sin_cupo_en_el_horario_falla(repositorio, servicio):
    repositorio.obtener("Safari", HORARIO).ocupados = 10

    with pytest.raises(SinCupoError):
        servicio.inscribir(crear_solicitud())


def test_inscripcion_de_grupo_mayor_a_los_cupos_restantes_falla(
    repositorio, servicio
):
    repositorio.obtener("Safari", HORARIO).ocupados = 9
    visitantes = [
        Visitante(nombre="Ana", dni="30111222", edad=25),
        Visitante(nombre="Luis", dni="31222333", edad=30),
    ]

    with pytest.raises(SinCupoError):
        servicio.inscribir(crear_solicitud(visitantes=visitantes))


def test_inscripcion_en_horario_sin_turno_de_la_actividad_falla(servicio):
    horario_sin_turno = datetime(2026, 10, 14, 11, 30)

    with pytest.raises(ActividadNoDisponibleError):
        servicio.inscribir(crear_solicitud(horario=horario_sin_turno))


def test_inscripcion_con_el_parque_cerrado_falla(calendario, servicio):
    calendario.abierto = False

    with pytest.raises(ParqueCerradoError):
        servicio.inscribir(crear_solicitud())
