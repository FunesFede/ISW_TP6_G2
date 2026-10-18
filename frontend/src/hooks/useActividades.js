import { useEffect, useState } from 'react'
import { obtenerActividades } from '../api/cliente'

export function useActividades () {
  const [actividades, setActividades] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let vigente = true
    obtenerActividades()
      .then((datos) => { if (vigente) setActividades(datos) })
      .catch((err) => { if (vigente) setError(err.message) })
      .finally(() => { if (vigente) setCargando(false) })
    return () => { vigente = false }
  }, [])

  return { actividades, cargando, error }
}
