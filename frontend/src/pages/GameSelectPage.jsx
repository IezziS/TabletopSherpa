import {useState} from 'react'
import { useNavigate } from 'react-router-dom'
import '../styles/GameSelectPage.css'
const GAMES = [
    { id: 'wh40k', label: "Warhammer 40,000", editions: ["10th","11th"]},
    { id: 'mtg', label: 'Magic: The Gathering', editions: ['Standard', 'Commander']},
]

function GameSelectPage() {
    const [selectedGame, setSelectedGame] = useState(null)
    const [selectedEdition, setSelectedEdition] = useState('')
    const navigate = useNavigate()

    function handleGameClick(game){
        setSelectedGame(game)
        setSelectedEdition('')
    }
    function handleStart(){
        if(!selectedGame || !selectedEdition) return
        navigate(`/chat/${selectedGame.id}?edition=${encodeURIComponent(selectedEdition)}`)

    }
    return(
         <div className="gameselect-container">
      <h1>Tabletop Sherpa</h1>

      <div className="gameselect-row">
        {GAMES.map((game) => (
          <button
            key={game.id}
            className={`gameselect-button theme-button-${game.id} ${selectedGame?.id === game.id ? 'selected' : ''}`}
            onClick={() => handleGameClick(game)}
          >
            {game.label}
          </button>
        ))}
      </div>

      {selectedGame && (
        <select
          className={`edition-selector theme-button-${selectedGame.id}`}
          value={selectedEdition}
          onChange={(e) => setSelectedEdition(e.target.value)}
        >
          <option value="">Select format/edition</option>
          {selectedGame.editions.map((edition) => (
            <option key={edition} value={edition}>{edition}</option>
          ))}
        </select>
      )}

      <button className='confirm-select' onClick={handleStart} disabled={!selectedGame || !selectedEdition}>
        Start
      </button>
    </div>
  )
}

export default GameSelectPage