import { useState } from 'react'
import './App.css'

function App() {

  const [message, setMessage] = useState('')
  const [response, setResponse] = useState('')
  
  const sendMessage = async()=>{

    console.log("Current message state is:", message);

    
    const response = await fetch('http://localhost:3000/api/chat',{
      method:'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    })

    const data = await response.json()
    setResponse(data.message)
  }

  return (
    <>
      <input 
      type="text"
      placeholder='send message'
      value={message}
      onChange={(e)=>{e.target.value}}
      />

      <button onClick={sendMessage}>Send</button>
      <p>Response : {response}</p>
    </>
  )
}

export default App
