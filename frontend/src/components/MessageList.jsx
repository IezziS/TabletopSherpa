import '../styles/MessageList.css'

function MessageList({ messages }) {
  return (
    <div className="messagelist-container">
      {messages.map((message, index) => (
        <div
          key={index}
          className={message.role === 'user' ? 'messagelist-user' : 'messagelist-sherpa'}
        >
          <div className={message.role === 'user' ? 'messagelist-bubble-user' : 'messagelist-bubble-sherpa'}>{message.text}</div>
        </div>
      ))}
    </div>
  )
}

export default MessageList