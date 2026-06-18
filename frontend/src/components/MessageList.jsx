
function MessageList({ messages}){
    return(
        <div>
            {messages.map((message, index) =>(
                <div key = {index}>
                    <strong>{message.role ==='user' ? 'You' : 'Sherpa'}:</strong>
                    <span> {message.text}</span>
                </div>
            ))}
        </div>
    )
}

export default MessageList