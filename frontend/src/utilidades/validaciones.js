// Validaciones de cada visitante. Replican las reglas del backend para
// avisar antes de enviar; el backend sigue siendo la fuente de verdad.

export const TALLES = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
const PATRON_DNI = /^\d{7,8}$/
const PATRON_EMAIL = /^[^@\s]+@[^@\s]+\.[^@\s]+$/

export function visitanteVacio () {
  return { nombre: '', dni: '', edad: '', talle: '' }
}

export function validarVisitante (visitante, actividad) {
  const errores = {}
  if (!visitante.nombre.trim()) {
    errores.nombre = 'Ingresá el nombre.'
  }
  if (!PATRON_DNI.test(visitante.dni)) {
    errores.dni = 'El DNI tiene 7 u 8 números, sin puntos.'
  }
  const edad = Number(visitante.edad)
  if (visitante.edad === '' || !Number.isInteger(edad) || edad < 0) {
    errores.edad = 'Ingresá la edad en años.'
  } else if (actividad && edad < actividad.edad_minima) {
    errores.edad = `${actividad.nombre} es desde los ${actividad.edad_minima} años.`
  }
  if (actividad?.requiere_talle && !TALLES.includes(visitante.talle)) {
    errores.talle = 'Elegí el talle.'
  }
  return errores
}

export function validarVisitantes (visitantes, actividad) {
  const errores = visitantes.map((visitante) => validarVisitante(visitante, actividad))
  const vistos = new Map()
  visitantes.forEach((visitante, indice) => {
    if (!visitante.dni) return
    if (vistos.has(visitante.dni)) {
      errores[indice].dni = `Este DNI ya está cargado en la persona ${vistos.get(visitante.dni) + 1}.`
    } else {
      vistos.set(visitante.dni, indice)
    }
  })
  return errores
}

export function emailValido (email) {
  return PATRON_EMAIL.test(email)
}

export function hayErrores (errores) {
  return errores.some((error) => Object.keys(error).length > 0)
}
