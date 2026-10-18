"""Dobles de prueba compartidos para reemplazar los puertos del dominio."""


class CalendarioFalso:
    def __init__(self, abierto=True):
        self.abierto = abierto

    def esta_abierto(self, fecha_hora):
        return self.abierto


class NotificadorEspia:
    def __init__(self):
        self.enviados = []

    def enviar_confirmacion(self, destinatario, inscripcion, qr_png):
        self.enviados.append((destinatario, inscripcion, qr_png))


class GeneradorQRFalso:
    def generar(self, contenido):
        return b"QR:" + contenido.encode()


class RelojFalso:
    def __init__(self, ahora):
        self.momento = ahora

    def ahora(self):
        return self.momento
