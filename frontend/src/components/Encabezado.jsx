import { USUARIO_ACTUAL } from '../datos/usuario'

export default function Encabezado () {
  return (
    <header className='encabezado'>
      <div className='encabezado__contenido'>
        <a className='encabezado__marca' href='/' aria-label='EcoHarmony Park, inicio'>
          <img src='/simbolo-ecoharmony.png' alt='' width='48' height='29' />
          <span className='encabezado__nombre'>EcoHarmony Park</span>
        </a>
        <span className='encabezado__usuario' title='Sesión de prueba'>
          <span className='encabezado__avatar' aria-hidden='true'>
            {USUARIO_ACTUAL.nombre.charAt(0)}
          </span>
          <span className='encabezado__usuario-nombre'>{USUARIO_ACTUAL.nombre}</span>
        </span>
      </div>
    </header>
  )
}
