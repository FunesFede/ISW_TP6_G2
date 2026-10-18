const DIA_SEMANA = new Intl.DateTimeFormat('es-AR', { weekday: 'short' })
const DIA_LARGO = new Intl.DateTimeFormat('es-AR', {
  weekday: 'long', day: 'numeric', month: 'long'
})
const FECHA_HORA = new Intl.DateTimeFormat('es-AR', {
  weekday: 'short', day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit'
})

export function diaSemanaCorto (fecha) {
  return DIA_SEMANA.format(fecha).replace('.', '')
}

export function diaLargo (fecha) {
  const texto = DIA_LARGO.format(fecha)
  return texto.charAt(0).toUpperCase() + texto.slice(1)
}

export function hora (fecha) {
  const horas = String(fecha.getHours()).padStart(2, '0')
  const minutos = String(fecha.getMinutes()).padStart(2, '0')
  return `${horas}:${minutos}`
}

export function fechaHora (fecha) {
  return FECHA_HORA.format(fecha)
}

export function personas (cantidad) {
  return cantidad === 1 ? '1 persona' : `${cantidad} personas`
}
