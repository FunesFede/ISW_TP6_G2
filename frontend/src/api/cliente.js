const URL_API = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000'

export class ErrorApi extends Error {
  constructor (mensaje, estado) {
    super(mensaje)
    this.estado = estado
  }
}

async function pedir (ruta, opciones = {}) {
  let respuesta
  try {
    respuesta = await fetch(`${URL_API}${ruta}`, {
      headers: { 'Content-Type': 'application/json' },
      ...opciones
    })
  } catch {
    throw new ErrorApi(
      'No pudimos conectarnos con el parque. Revisá tu conexión e intentá de nuevo.',
      0
    )
  }
  const datos = await respuesta.json().catch(() => null)
  if (!respuesta.ok) {
    throw new ErrorApi(mensajeDeError(datos), respuesta.status)
  }
  return datos
}

function mensajeDeError (datos) {
  const detalle = datos?.detail
  if (typeof detalle === 'string') return detalle
  if (Array.isArray(detalle)) {
    const campo = detalle[0]?.loc?.at(-1)
    if (campo === 'email') return 'Revisá el correo electrónico: no tiene un formato válido.'
    return 'Hay datos con un formato inválido. Revisá el formulario.'
  }
  return 'No pudimos completar la operación. Intentá de nuevo.'
}

export function obtenerActividades () {
  return pedir('/actividades')
}

export function obtenerTurnos (actividad, fecha) {
  const params = new URLSearchParams({ fecha })
  return pedir(`/actividades/${encodeURIComponent(actividad)}/turnos?${params}`)
}

export function crearInscripcion (inscripcion) {
  return pedir('/inscripciones', {
    method: 'POST',
    body: JSON.stringify(inscripcion)
  })
}

export function obtenerCorreo (codigo) {
  return pedir(`/inscripciones/${encodeURIComponent(codigo)}/correo`)
}
