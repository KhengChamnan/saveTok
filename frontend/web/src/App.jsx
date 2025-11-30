import { useState } from 'react'
import axios from 'axios'
import './App.css'

// API base URL - uses environment variable in production, empty string for local dev (uses proxy)
const API_URL = import.meta.env.VITE_API_URL || ''

function App() {
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [videoInfo, setVideoInfo] = useState(null)

  const handleDownload = async () => {
    if (!url.trim()) {
      setError('Please enter a TikTok URL')
      return
    }

    if (!url.includes('tiktok.com')) {
      setError('Please enter a valid TikTok URL')
      return
    }

    setLoading(true)
    setError('')
    setVideoInfo(null)

    try {
      // Request download
      const response = await axios.post(`${API_URL}/api/download`, { url })
      
      setVideoInfo({
        title: response.data.title,
        duration: response.data.duration,
      })

      // Trigger file download
      const downloadUrl = `${API_URL}${response.data.download_url}`
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = response.data.filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)

    } catch (err) {
      const errorMessage = err.response?.data?.detail || 'Failed to download video. Please try again.'
      setError(errorMessage)
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleDownload()
    }
  }

  return (
    <div className="container">
      <div className="card">
        <div className="logo">
          <span className="logo-icon">📱</span>
          <h1>TikTok Downloader</h1>
        </div>
        
        <p className="subtitle">
          Paste a TikTok video link to download it instantly
        </p>

        <div className="input-group">
          <input
            type="text"
            placeholder="https://www.tiktok.com/@user/video/..."
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
          <button onClick={handleDownload} disabled={loading}>
            {loading ? (
              <span className="spinner"></span>
            ) : (
              '⬇️ Download'
            )}
          </button>
        </div>

        {error && (
          <div className="error">
            ⚠️ {error}
          </div>
        )}

        {videoInfo && (
          <div className="success">
            <p>✅ Downloaded: {videoInfo.title}</p>
            <p className="duration">Duration: {videoInfo.duration}s</p>
          </div>
        )}

        <div className="disclaimer">
          <p>⚠️ For personal use only. Respect content creators' rights.</p>
        </div>
      </div>
    </div>
  )
}

export default App
