
import { useEffect, useState } from 'react'

function Chatbot({ candidateInfo, careerRoadmap }) {

  const [message, setMessage] = useState('')
  const [chatHistory, setChatHistory] = useState([])
  const [loading, setLoading] = useState(false)

  const [sessionId] = useState(() => {
    let id = localStorage.getItem('career_chat_session_id')

    if (!id) {
      id = crypto.randomUUID()
      localStorage.setItem('career_chat_session_id', id)
    }

    return id
  })

  // Format AI Response
  const formatResponse = (text) => {
    return text
      .replace(/\\\*/g, '*')
      .replace(/\s*(\*\*\d+\.)/g, '\n\n$1')
      .replace(/\s+-\s+/g, '\n   • ')
      .trim()
  }

  // Load Chat History
  useEffect(() => {
    const loadChatHistory = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:8000/api/ai/chat-history/?session_id=${encodeURIComponent(sessionId)}`
        )

        const data = await response.json()

        if (!response.ok) {
          throw new Error(data.error || 'Unable to load history')
        }

        setChatHistory(data.messages || [])

      } catch (error) {
        console.error('Chat History Error:', error)
      }
    }

    loadChatHistory()
  }, [sessionId])

  // Send Message
  const sendMessage = async () => {
    if (!message.trim() || loading) return

    const userMessage = message.trim()
    const previousHistory = [...chatHistory]

    setChatHistory(prev => [
      ...prev,
      { role: 'user', text: userMessage }
    ])

    setMessage('')
    setLoading(true)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/chat/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: userMessage,
            candidate_info: candidateInfo,
            career_roadmap: careerRoadmap,
            chat_history: previousHistory,
            session_id: sessionId
          })
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Chat request failed')
      }

      setChatHistory(prev => [
        ...prev,
        {
          role: 'assistant',
          text: data.response || 'No response received.'
        }
      ])

    } catch (error) {
      setChatHistory(prev => [
        ...prev,
        {
          role: 'assistant',
          text: `Error: ${error.message}`
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  // Clear Chat from Database
  const clearChat = async () => {

    if (loading || chatHistory.length === 0) return

    const confirmed = window.confirm(
      'Are you sure you want to delete all chat messages?'
    )

    if (!confirmed) return

    setLoading(true)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/delete-chat-history/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            session_id: sessionId
          })
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Unable to delete chat')
      }

      setChatHistory([])
      alert('Chat history deleted successfully!')

    } catch (error) {
      alert(`Delete Error: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="card">

      <h2>AI Career Chatbot</h2>

      <p>
        Ask questions about your resume, career and learning roadmap.
      </p>

      <div className="chat-messages">

        {chatHistory.length === 0 && (
          <p>
            Hello! I am your AI Career Assistant.
            Ask me anything about your career.
          </p>
        )}

        {chatHistory.map((chat, index) => (
          <div key={index} className="chat-message">

            <strong>
              {chat.role === 'user' ? 'You' : 'AI Assistant'}:
            </strong>

            <p style={{
              whiteSpace: 'pre-wrap',
              lineHeight: '1.8'
            }}>
              {chat.role === 'assistant'
                ? formatResponse(chat.text)
                : chat.text}
            </p>

          </div>
        ))}

        {loading && <p>AI is thinking...</p>}

      </div>

      <div className="chat-input">

        <input
          type="text"
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter') sendMessage()
          }}
          placeholder="Ask your career question..."
          disabled={loading}
        />

        <button
          onClick={sendMessage}
          disabled={loading || !message.trim()}
        >
          {loading ? 'Sending...' : 'Send'}
        </button>

        <button
          onClick={clearChat}
          disabled={loading || chatHistory.length === 0}
        >
          Clear Chat
        </button>

      </div>

    </section>
  )
}

export default Chatbot
