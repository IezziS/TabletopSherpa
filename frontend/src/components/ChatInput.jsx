import { useState } from "react";
import '../styles/ChatInput.css'



function ChatInput({onSend , disabled}) {
    const [inputValue , setInputValue] = useState('')

    function handleSend(){
        if (inputValue.trim() ==='') return
        onSend(inputValue)
        setInputValue('')
    }
    function handleKeyDown(e) {
        if (e.key === 'Enter') handleSend()

    }
    return (
        <div className="chat-input-bubble">
            <input
                className="inputfield"
                type = "text"
                value = {inputValue}
                onChange = {(e) => setInputValue(e.target.value)}
                onKeyDown = {handleKeyDown}
                disabled={disabled}
                placeholder = "Ask about rules..."
            />
            <button className="send-it" onClick= {handleSend}>Send</button>
        </div>
    )
}

export default ChatInput