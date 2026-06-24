import { useState } from 'react'
import axios from 'axios'
import './App.css'

const QUICK_CROPS = ['Wheat', 'Onion', 'Tomato', 'Potato', 'Rice', 'Cabbage']
const BACKEND_URL = 'http://127.0.0.1:8000'

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Namaste! 🌾 Main aapka AI Farmer Sales Bot hoon. Kisi crop ka naam type karo ya neeche button dabao, main aapko best mandi price bataunga.' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendQuery = async (cropName) => {
    if (!cropName.trim()) return

    setMessages(prev => [...prev, { sender: 'user', text: cropName }])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.get(`${BACKEND_URL}/best-mandi-smart/${cropName.toLowerCase()}`)
      const data = response.data

      if (data.best_option) {
        const best = data.best_option
        const sourceNote = best.source === 'live_api' ? '📡 Live data' : '📦 Demo data'
        const botText = `${cropName} ke liye best mandi: **${best.mandi}, ${best.state}**\n\nModal Price: ₹${best.modal_price}/quintal\nNet Price (after transport): ₹${best.net_price_per_quintal}/quintal\n\n${sourceNote}`
        setMessages(prev => [...prev, { sender: 'bot', text: botText }])
      } else {
        setMessages(prev => [...prev, { sender: 'bot', text: `Sorry, '${cropName}' ke liye data nahi mila. Available crops try karo: Wheat, Onion, Tomato, Potato, Rice, Cabbage.` }])
      }
    } catch (error) {
      setMessages(prev => [...prev, { sender: 'bot', text: 'Kuch error aaya backend se connect karne mein. Backend server chal raha hai check karo.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleSend = () => {
    sendQuery(input)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSend()
  }

  return (
    <div className="app-container">
      <header className="chat-header">
        <h1>🌾 AI Farmer Sales Bot</h1>
        <p>Real-time mandi prices, best price finder</p>
      </header>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <p style={{ whiteSpace: 'pre-line' }}>{msg.text}</p>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <p>Mandi data check kar rahe hain... ⏳</p>
          </div>
        )}
      </div>

      <div className="quick-buttons">
        {QUICK_CROPS.map(crop => (
          <button key={crop} onClick={() => sendQuery(crop)} disabled={loading}>
            {crop}
          </button>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Crop ka naam type karo (jaise: wheat)"
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  )
}

export default App