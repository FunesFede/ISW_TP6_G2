import { useCallback, useEffect, useState } from 'react'
import { obtenerTurnos } from '../api/cliente'

export function useTurnos (actividad, fecha) {
  const [turnos, setTurnos] = useState([])
  const [cargando, setCargando] = useState(false)
  const [error, setError] = useState(null)
  const [version, setVersion] = useState(0)

  useEffect(() => {
    if (!actividad || !fecha) {
      setTurnos([])
      return
    }
    let vigente = true
    setCargando(true)
    setError(null)
    obtenerTurnos(actividad, fecha)
      .then((datos) => { if (vigente) setTurnos(datos) })
      .catch((err) => { if (vigente) setError(err.message) })
      .finally(() => { if (vigente) setCargando(false) })
    return () => { vigente = false }
  }, [actividad, fecha, version])

  const recargar = useCallback(() => setVersion((v) => v + 1), [])

  return { turnos, cargando, error, recargar }
}
