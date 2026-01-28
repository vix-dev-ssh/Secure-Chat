import { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState("Connecting...")

  useEffect(() => {
    // Fetch from the live backend
    fetch(`${import.meta.env.VITE_API_URL}/health`)
      .then(res => res.json())
      .then(data => setStatus(`Backend Status: ${data.message}`))
      .catch(err => setStatus(`Error: ${err.message}`))
  }, [])

  return (
    <div style={{ padding: "50px", fontFamily: "sans-serif", textAlign: "center" }}>
      <h1>Secure Chat</h1>
      <div style={{ 
        padding: "20px", 
        border: "2px solid #333", 
        borderRadius: "10px",
        display: "inline-block",
        marginTop: "20px"
      }}>
        <h2>System Status</h2>
        <p style={{ color: status.includes("Error") ? "red" : "green", fontWeight: "bold" }}>
          {status}
        </p>
      </div>
    </div>
  )
}

export default App