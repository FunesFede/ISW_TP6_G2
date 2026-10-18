from datetime import datetime
from zoneinfo import ZoneInfo

ZONA_PARQUE = ZoneInfo("America/Argentina/Cordoba")


class RelojSistema:
    """Hora actual en la zona del parque.

    Devuelve un datetime sin zona horaria para compararlo con los
    horarios de los turnos, que también se guardan sin zona.
    """

    def ahora(self) -> datetime:
        return datetime.now(ZONA_PARQUE).replace(tzinfo=None)
