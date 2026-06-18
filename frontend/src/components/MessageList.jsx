
function MessageList({ messages}){
    return(
        <div>
            {messages.map((message, index) =>(
                <div key = {index}
                style={{
                    display: "flex",
                    justifyContent:message.role ==='user'? 'flex-end':'flex-start'
                }}>
                    
                    <span> {message.text}</span>
                </div>
            ))}
        </div>
    )
}

export default MessageList