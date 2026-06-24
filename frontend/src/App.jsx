import { useState } from 'react'
import axios from 'axios'
import './App.css'

const QUICK_CROPS = ['Wheat', 'Onion', 'Tomato', 'Potato', 'Rice', 'Cabbage']
const BACKEND_URL = 'http://127.0.0.1:8000'

function App() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Namaste! 🌾 Main aapka AI Farmer Sales Bot hoon.\n\n📊 Crop ka naam type karo (jaise: wheat) - best mandi price ke liye\n💰 Negotiate karne ke liye type karo: "negotiate <crop> <offer_price> <quantity>"\nExample: negotiate onion 1800 5' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const handleMandiQuery = async (cropName) => {
    const response = await axios.get(`${BACKEND_URL}/best-mandi-smart/${cropName.toLowerCase()}`)
    const data = response.data

    if (data.best_option) {
      const best = data.best_option
      const sourceNote = best.source === 'live_api' ? '📡 Live data' : '📦 Demo data'
      return `${cropName} ke liye best mandi: **${best.mandi}, ${best.state}**\n\nModal Price: ₹${best.modal_price}/quintal\nNet Price (after transport): ₹${best.net_price_per_quintal}/quintal\n\n${sourceNote}`
    } else {
      return `Sorry, '${cropName}' ke liye data nahi mila. Available crops try karo: Wheat, Onion, Tomato, Potato, Rice, Cabbage.`
    }
  }

  const handleNegotiateQuery = async (crop, offerPrice, quantity) => {
    const response = await axios.get(`${BACKEND_URL}/evaluate-offer/${crop.toLowerCase()}`, {
      params: { offer_price: offerPrice, quantity_quintal: quantity }
    })
    const data = response.data

    const verdictEmoji = data.verdict === 'accept' ? '✅' : data.verdict === 'counter' ? '🤝' : '⚠️'

    let text = `${verdictEmoji} **Negotiation Analysis: ${crop}**\n\n`
    text += `Trader Offer: ₹${data.offer_price}/quintal\n`
    text += `Mandi Average: ₹${data.mandi_average_price}/quintal\n`
    text += `Difference: ${data.percent_difference}%\n\n`
    text += `${data.advice}\n\n`
    if (data.potential_loss_total > 0) {
      text += `⚠️ Agar accept karte ho toh total loss: ₹${data.potential_loss_total}`
    }
    return text
  }

  const parseNegotiateCommand = (text) => {
    // Format: "negotiate onion 1800 5"
    const parts = text.trim().split(/\s+/)
    if (parts.length >= 3 && parts[0].toLowerCase() === 'negotiate') {
      const crop = parts[1]
      const offerPrice = parseFloat(parts[2])
      const quantity = parts[3] ? parseFloat(parts[3]) : 1
      if (!isNaN(offerPrice)) {
        return { crop, offerPrice, quantity }
      }
    }
    return null
  }

  const sendQuery = async (userText) => {
    if (!userText.trim()) return

    setMessages(prev => [...prev, { sender: 'user', text: userText }])
    setInput('')
    setLoading(true)

    try {
      const negotiateParams = parseNegotiateCommand(userText)
      let botText

      if (negotiateParams) {
        botText = await handleNegotiateQuery(negotiateParams.crop, negotiateParams.offerPrice, negotiateParams.quantity)
      } else {
        botText = await handleMandiQuery(userText)
      }

      setMessages(prev => [...prev, { sender: 'bot', text: botText }])
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
        <p>Real-time mandi prices, negotiation coach</p>
      </header>

      <div className="chat-window">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.sender}`}>
            <p style={{ whiteSpace: 'pre-line' }}>{msg.text}</p>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <p>Check kar rahe hain... ⏳</p>
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
          placeholder="Crop naam ya: negotiate onion 1800 5"
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  )
}

export default App