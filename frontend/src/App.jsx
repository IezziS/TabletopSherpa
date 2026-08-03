import {BrowserRouter, Routes, Route} from 'react-router-dom'
import GameSelectPage from './pages/GameSelectPage'
import ChatPage from './pages/ChatPage'


function App() {
  return(
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<GameSelectPage />} />
        <Route path="/chat/:game" element={<ChatPage />} /> 
      </Routes>
    </BrowserRouter>
  )
}
export default App
