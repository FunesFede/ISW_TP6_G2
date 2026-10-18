import terminos from '../datos/terminos.json'

// Orden en que se muestran los términos: primero lo propio de la
// actividad y después las condiciones comunes a todas.
export function seccionesDeTerminos (actividad) {
  const { comunes, actividades } = terminos
  return [
    actividades[actividad].requisitos,
    comunes.inscripcion,
    comunes.datos,
    comunes.dia,
    comunes.cambios,
    comunes.privacidad
  ]
}
