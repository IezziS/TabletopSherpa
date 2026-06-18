import { useState } from 'react'
import ChatInput from './components/ChatInput'
import MessageList from './components/MessageList'

const apiAddr = 'http://localhost:8000/'

function App() {
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  async function handleSend(userText){
    const userMessage = {role: 'user', text: userText}
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    const addr = apiAddr+'chat/'

    try{
      const response = await fetch(addr+'ask', {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({question: userText, game: 'Wh40k', edition: '10th'})
      })
      const data = await response.json()

      const sherpaMessage = {role: 'sherpa', text: data.answer}
      setMessages((prev) =>[...prev, sherpaMessage])
    }catch (error){
      const errorMessage = {role: 'sherpa', text: 'Something went wrong. Try again.'+error}
      setMessages((prev) => [...prev, errorMessage])
    }finally{
      setIsLoading(false)
    }
  }

  return (
    <div>
      <h1>TABLETOP SHERPA</h1>
      <MessageList messages = {messages}/>
      <ChatInput onSend={handleSend} disabled={isLoading}/>
      {isLoading && <p> Thinking ... </p>}
    </div>
  )
}

export default App
