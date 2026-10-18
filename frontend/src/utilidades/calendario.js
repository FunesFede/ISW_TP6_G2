// Reglas del calendario del parque (FAQ 1, 11, 12 y 23). El backend vuelve
// a validar todo; acá solo se usan para guiar al visitante.

export const LUNES = 1
export const FERIADOS = ['12-25', '01-01']
export const APERTURA_PARQUE = { horas: 8, minutos: 30 }
export const CIERRE_PARQUE = { horas: 19, minutos: 0 }
export const PRIMER_TURNO = 9
export const ULTIMO_TURNO = 17
export const HORAS_APERTURA_INSCRIPCION = 24
export const MINUTOS_CIERRE_INSCRIPCION = 15

const MS_POR_MINUTO = 60 * 1000
const MS_POR_HORA = 60 * MS_POR_MINUTO

export function aFechaIso (fecha) {
  const anio = fecha.getFullYear()
  const mes = String(fecha.getMonth() + 1).padStart(2, '0')
  const dia = String(fecha.getDate()).padStart(2, '0')
  return `${anio}-${mes}-${dia}`
}

export function desdeFechaIso (iso) {
  const [anio, mes, dia] = iso.split('-').map(Number)
  return new Date(anio, mes - 1, dia)
}

export function desdeHorarioIso (iso) {
  const [fecha, hora] = iso.split('T')
  const [horas, minutos] = hora.split(':').map(Number)
  const resultado = desdeFechaIso(fecha)
  resultado.setHours(horas, minutos, 0, 0)
  return resultado
}

export function esFeriado (fecha) {
  return FERIADOS.includes(aFechaIso(fecha).slice(5))
}

export function parqueAbreElDia (fecha) {
  return fecha.getDay() !== LUNES && !esFeriado(fecha)
}

// Último turno que puede tener la inscripción abierta: el de mañana a la
// misma hora que ahora. Un día es elegible si alguno de sus turnos ya abrió.
export function inscripcionHabilitadaElDia (fecha, ahora) {
  if (!parqueAbreElDia(fecha)) return false
  const primerTurno = new Date(fecha)
  primerTurno.setHours(PRIMER_TURNO, 0, 0, 0)
  const ultimoTurno = new Date(fecha)
  ultimoTurno.setHours(ULTIMO_TURNO, 0, 0, 0)
  const aperturaPrimero = primerTurno.getTime() - HORAS_APERTURA_INSCRIPCION * MS_POR_HORA
  const cierreUltimo = ultimoTurno.getTime() - MINUTOS_CIERRE_INSCRIPCION * MS_POR_MINUTO
  return ahora.getTime() >= aperturaPrimero && ahora.getTime() <= cierreUltimo
}

export function proximosDias (ahora, cantidad) {
  return Array.from({ length: cantidad }, (_, indice) => {
    const dia = new Date(ahora)
    dia.setHours(0, 0, 0, 0)
    dia.setDate(dia.getDate() + indice)
    return dia
  })
}

export function aperturaInscripcion (inicioTurno) {
  return new Date(inicioTurno.getTime() - HORAS_APERTURA_INSCRIPCION * MS_POR_HORA)
}

export function cierreInscripcion (inicioTurno) {
  return new Date(inicioTurno.getTime() - MINUTOS_CIERRE_INSCRIPCION * MS_POR_MINUTO)
}

// Estado que ve el visitante para cada turno.
export function estadoTurno (turno, cantidadPersonas, ahora) {
  const inicio = desdeHorarioIso(turno.horario)
  if (!turno.inscripcion_abierta) {
    return ahora < aperturaInscripcion(inicio) ? 'por-abrir' : 'cerrado'
  }
  if (turno.cupos_disponibles === 0) return 'agotado'
  if (turno.cupos_disponibles < cantidadPersonas) return 'insuficiente'
  return 'disponible'
}
