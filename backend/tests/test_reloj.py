from datetime import datetime, timedelta, timezone

from app.infraestructura.reloj import ZONA_PARQUE, RelojSistema


def test_reloj_del_sistema_devuelve_la_hora_local_del_parque_sin_zona():
    ahora = RelojSistema().ahora()

    esperado = datetime.now(timezone.utc).astimezone(ZONA_PARQUE)
    assert ahora.tzinfo is None
    assert abs(ahora - esperado.replace(tzinfo=None)) < timedelta(seconds=5)
