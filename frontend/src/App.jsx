import { useState } from 'react'
import './App.css'

function App() {
  const [text, setText] = useState('')
  const [response, setResponse] = useState('')

  const [file, setFile] = useState(null)
  const [message, setMessage] = useState('')

  const handleFileChange = async (e) => {
    try {
      setFile(e.target.files[0])
    } catch (error) {
      console.log("Error setting file:", error.message)
    }
  }

  const uploadFile = async () => {
    if (!file) {
      alert("Select a file first");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        body: formData, 
      });

      const data = await response.json();
      if(!response.ok){
        setMessage(`Error: ${data.detail}`);
        return
      }

      setMessage(`Uploaded: ${data.filename}`);
      
      
    } catch (error) {
      console.error("Upload failed:", error);
    }
  }

  const sendText = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/send', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          text: text,
        }),
      })

      const data = await res.json()
      setResponse(data.received_text)

    } catch (error) {
      console.log("Text ping error:", error.message)
    }
  }

  return (
    <>
      <div>
        <input
          type="text"
          placeholder='Stell irgendeine Frage'
          value={text}
          onChange={(e) => { setText(e.target.value) }}
        />
        <h5>you : <p>{response}</p></h5>

        <button onClick={sendText}>Send</button>
        

        <input 
          type="file"
          onChange={handleFileChange}
        />

      
        <button onClick={uploadFile}>Upload Document</button>
        <p>File Response : {message}</p>

      </div>
    </>
  )
}

export default App