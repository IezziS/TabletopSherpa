import { useState } from "react";


function ChatInput({onSend}) {
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
        <div>
            <input
                type = "text"
                value = {inputValue}
                onChange = {(e) => setInputValue(e.target.value)}
                onKeyDown = {handleKeyDown}
                placeholder = "Ask about rules..."
            />
            <button onClick= {handleSend}>Send</button>
        </div>
    )
}

export default ChatInput