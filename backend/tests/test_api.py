import base64
from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from app.api.aplicacion import crear_aplicacion
from app.dominio.modelos import Turno
from app.infraestructura.calendario_parque import CalendarioParqueSemanal
from app.infraestructura.repositorio_inscripciones import (
    RepositorioInscripcionesEnMemoria,
)
from app.infraestructura.repositorio_turnos import (
    RepositorioTurnosEnMemoria,
)
from tests.dobles import GeneradorQRFalso, NotificadorEspia, RelojFalso

HORARIO = datetime(2026, 10, 14, 10, 0)  # miércoles


@pytest.fixture
def repositorio():
    return RepositorioTurnosEnMemoria([
        Turno(actividad="Safari", inicio=HORARIO, cupo_total=10),
        Turno(actividad="Tirolesa", inicio=HORARIO, cupo_total=2),
    ])


@pytest.fixture
def notificador():
    return NotificadorEspia()


@pytest.fixture
def cliente(repositorio, notificador):
    aplicacion = crear_aplicacion(
        repositorio_turnos=repositorio,
        calendario_parque=CalendarioParqueSemanal(),
        notificador=notificador,
        generador_qr=GeneradorQRFalso(),
        reloj=RelojFalso(HORARIO - timedelta(hours=2)),
        repositorio_inscripciones=RepositorioInscripcionesEnMemoria(),
    )
    return TestClient(aplicacion)


def cuerpo_inscripcion(**cambios):
    cuerpo = {
        "actividad": "Safari",
        "horario": HORARIO.isoformat(),
        "email": "ana@mail.com",
        "acepta_terminos": True,
        "visitantes": [{"nombre": "Ana", "dni": "30111222", "edad": 25}],
    }
    cuerpo.update(cambios)
    return cuerpo


def test_post_inscripcion_valida_responde_201(cliente, notificador):
    respuesta = cliente.post("/inscripciones", json=cuerpo_inscripcion())

    assert respuesta.status_code == 201
    datos = respuesta.json()
    assert datos["codigo"]
    assert datos["actividad"] == "Safari"
    assert datos["cantidad_personas"] == 1
    assert len(notificador.enviados) == 1


def test_post_inscripcion_a_actividad_inexistente_responde_404(cliente):
    respuesta = cliente.post(
        "/inscripciones", json=cuerpo_inscripcion(actividad="Rafting")
    )

    assert respuesta.status_code == 404


def test_post_inscripcion_sin_cupo_responde_409(cliente):
    visitantes = [
        {"nombre": f"P{i}", "dni": str(30111220 + i), "edad": 20,
         "talle": "M"}
        for i in range(3)
    ]

    respuesta = cliente.post(
        "/inscripciones",
        json=cuerpo_inscripcion(actividad="Tirolesa", visitantes=visitantes),
    )

    assert respuesta.status_code == 409
    assert "cupo" in respuesta.json()["detail"].lower()


@pytest.mark.parametrize(
    "cambios",
    [
        {"acepta_terminos": False},
        {"horario": "2026-10-12T10:00:00"},  # lunes, parque cerrado
        {"horario": "2026-10-14T11:30:00"},  # sin turno de Safari
        {"actividad": "Tirolesa"},           # requiere talle
        {"visitantes": []},
    ],
    ids=["sin-terminos", "parque-cerrado", "sin-turno", "sin-talle",
         "sin-visitantes"],
)
def test_post_inscripcion_con_regla_de_negocio_incumplida_responde_422(
    cliente, cambios
):
    respuesta = cliente.post(
        "/inscripciones", json=cuerpo_inscripcion(**cambios)
    )

    assert respuesta.status_code == 422
    assert isinstance(respuesta.json()["detail"], str)


def test_post_inscripcion_con_email_invalido_responde_422(cliente):
    respuesta = cliente.post(
        "/inscripciones", json=cuerpo_inscripcion(email="no-es-un-mail")
    )

    assert respuesta.status_code == 422


def test_get_actividades_lista_las_cuatro_con_sus_requisitos(cliente):
    respuesta = cliente.get("/actividades")

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"nombre": "Tirolesa", "requiere_talle": True, "edad_minima": 8,
         "cupo_por_turno": 10},
        {"nombre": "Safari", "requiere_talle": False, "edad_minima": 0,
         "cupo_por_turno": 8},
        {"nombre": "Palestra", "requiere_talle": True, "edad_minima": 12,
         "cupo_por_turno": 12},
        {"nombre": "Jardinería", "requiere_talle": False, "edad_minima": 0,
         "cupo_por_turno": 12},
    ]


def test_get_turnos_de_una_actividad_en_una_fecha(cliente, repositorio):
    repositorio.guardar(Turno(
        actividad="Safari", inicio=datetime(2026, 10, 14, 15, 0),
        cupo_total=10, ocupados=10,
    ))
    repositorio.guardar(Turno(
        actividad="Safari", inicio=datetime(2026, 10, 15, 10, 0),
        cupo_total=10,
    ))

    respuesta = cliente.get(
        "/actividades/Safari/turnos", params={"fecha": "2026-10-14"}
    )

    assert respuesta.status_code == 200
    assert respuesta.json() == [
        {"horario": "2026-10-14T10:00:00", "cupos_disponibles": 10,
         "inscripcion_abierta": True},
        {"horario": "2026-10-14T15:00:00", "cupos_disponibles": 0,
         "inscripcion_abierta": True},
    ]


def test_get_turnos_de_actividad_inexistente_responde_404(cliente):
    respuesta = cliente.get(
        "/actividades/Rafting/turnos", params={"fecha": "2026-10-14"}
    )

    assert respuesta.status_code == 404


def test_get_turnos_indica_si_la_inscripcion_esta_abierta(
    cliente, repositorio
):
    # El reloj marca 14/10/2026 a las 8:00.
    repositorio.guardar(Turno(
        actividad="Safari", inicio=datetime(2026, 10, 14, 8, 10),
        cupo_total=8,
    ))
    repositorio.guardar(Turno(
        actividad="Safari", inicio=datetime(2026, 10, 15, 9, 0),
        cupo_total=8,
    ))

    hoy = cliente.get(
        "/actividades/Safari/turnos", params={"fecha": "2026-10-14"}
    ).json()
    manana = cliente.get(
        "/actividades/Safari/turnos", params={"fecha": "2026-10-15"}
    ).json()

    assert hoy[0]["inscripcion_abierta"] is False    # cierra a las 7:55
    assert hoy[1]["inscripcion_abierta"] is True     # turno de las 10:00
    assert manana[0]["inscripcion_abierta"] is False  # abre el 14 a las 9


def test_post_inscripcion_superpuesta_responde_409(cliente):
    cliente.post("/inscripciones", json=cuerpo_inscripcion())

    respuesta = cliente.post("/inscripciones", json=cuerpo_inscripcion())

    assert respuesta.status_code == 409


def test_get_correo_devuelve_el_mail_de_confirmacion_con_el_qr(cliente):
    codigo = cliente.post(
        "/inscripciones", json=cuerpo_inscripcion()
    ).json()["codigo"]

    respuesta = cliente.get(f"/inscripciones/{codigo}/correo")

    assert respuesta.status_code == 200
    correo = respuesta.json()
    assert correo["destinatario"] == "ana@mail.com"
    assert "Safari" in correo["asunto"]
    assert codigo in correo["cuerpo"]
    assert "Ana" in correo["cuerpo"]
    assert correo["adjunto"]["nombre"] == f"inscripcion-{codigo}.png"
    assert correo["adjunto"]["tipo"] == "image/png"
    contenido = base64.b64decode(correo["adjunto"]["contenido_base64"])
    assert contenido == b"QR:" + codigo.encode()


def test_get_correo_de_inscripcion_inexistente_responde_404(cliente):
    respuesta = cliente.get("/inscripciones/NOEXISTE/correo")

    assert respuesta.status_code == 404
