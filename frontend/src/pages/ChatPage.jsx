import { useState } from 'react'
import {useParams , useSearchParams} from 'react-router-dom'
import ChatInput from '../components/ChatInput'
import MessageList from '../components/MessageList'
import '../styles/ChatPage.css'

const apiAddr = 'http://localhost:8000/'

function ChatPage() {
  const {game} = useParams()
  const [searchParams] = useSearchParams()
  const [messages, setMessages] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const edition = searchParams.get('edition')


  async function handleSend(userText){
    const userMessage = {role: 'user', text: userText}
    setMessages((prev) => [...prev, userMessage])
    setIsLoading(true)

    const addr = apiAddr+'chat/'

    try{
      const response = await fetch(addr+'ask', {
        method: 'POST',
        headers: {'Content-Type' : 'application/json'},
        body: JSON.stringify({question: userText, game: game, edition: edition})
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
    <div className={`theme-${game}`}>
      <h1 className='nameplate'>TABLETOP SHERPA</h1>
      <MessageList messages = {messages}/>
      <ChatInput onSend={handleSend} disabled={isLoading}/>
      {isLoading && <p className='thinking'> Thinking ... </p>}
    </div>
  )
}

export default ChatPage