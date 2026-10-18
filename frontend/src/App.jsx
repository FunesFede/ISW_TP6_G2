import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ConfirmacionView from './views/ConfirmacionView'
import CorreoView from './views/CorreoView'
import InscripcionView from './views/InscripcionView'

export default function App () {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<InscripcionView />} />
        <Route path='/confirmacion/:codigo' element={<ConfirmacionView />} />
        <Route path='/correo/:codigo' element={<CorreoView />} />
      </Routes>
    </BrowserRouter>
  )
}
