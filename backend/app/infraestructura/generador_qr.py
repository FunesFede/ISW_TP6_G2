import io

import qrcode


class GeneradorQRPng:

    def generar(self, contenido: str) -> bytes:
        imagen = qrcode.make(contenido)
        buffer = io.BytesIO()
        imagen.save(buffer, format="PNG")
        return buffer.getvalue()
