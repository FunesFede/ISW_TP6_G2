import { useEffect, useState } from 'react'

// Hora actual que se actualiza sola, para que los turnos cambien de estado
// sin recargar la página.
export function useAhora (intervaloMs = 30000) {
  const [ahora, setAhora] = useState(() => new Date())

  useEffect(() => {
    const id = setInterval(() => setAhora(new Date()), intervaloMs)
    return () => clearInterval(id)
  }, [intervaloMs])

  return ahora
}
