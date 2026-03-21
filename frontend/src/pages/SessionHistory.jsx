import React, { useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

const SessionDetailModal = ({ session, onClose }) => {
  if (!session) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="session-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>{session.title}</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>

        <div className="modal-content">
          {/* Session Video */}
  <div className="detail-section">
    <h3>Recorded Session</h3>

    <video
      controls
      width="100%"
      style={{ borderRadius: "10px" }}
      src={`http://localhost:8000/videos/${session.video_path.split("/").pop()}`}
    />
  </div>

          {/* Session Overview */}
          <div className="detail-section">
            <h3>Session Overview</h3>
            <div className="detail-grid">
              <div className="detail-item">
                <label>Date</label>
                <span>{session.date}</span>
              </div>
              <div className="detail-item">
                <label>Duration</label>
                <span>{session.duration}</span>
              </div>
              <div className="detail-item">
                <label>Type</label>
                <span>{session.type}</span>
              </div>
              <div className="detail-item">
                <label>Status</label>
                <span className="status-badge">{session.status}</span>
              </div>
            </div>
          </div>

          {/* Overall Score */}
          <div className="detail-section">
            <h3>Overall Performance Score</h3>
            <div className="score-display">
              <div className={`large-score-circle ${session.score >= 8.5 ? 'excellent' : session.score >= 8 ? 'very-good' : 'good'}`}>
                <span className="large-score">{session.score.toFixed(1)}</span>
                <span className="large-score-max">/10</span>
              </div>
              <div className="score-description">
                <p>Your performance in this session was <strong>{session.score >= 8.5 ? 'outstanding' : session.score >= 8 ? 'very good' : 'good'}</strong>.</p>
              </div>
            </div>
          </div>

          {/* Detailed Metrics */}
          <div className="detail-section">
            <h3>Detailed Metrics Breakdown</h3>
            <div className="metrics-breakdown">
              {Object.entries(session.metrics).map(([key, value]) => (
                <div key={key} className="metric-row">
                  <div className="metric-left">
                    <span className="metric-label">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                    <span className="metric-score">{typeof value === 'number' ? value.toFixed(1) : value}</span>
                  </div>
                  <div className="metric-bar-container">
                    <div className="metric-bar">
                      <div 
                        className="metric-bar-fill" 
                        style={{ width: `${(value / 10) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Feedback */}
          <div className="detail-section">
            <h3>AI Feedback Analysis</h3>
            <div className="feedback-list">
              {Array.isArray(session.feedback) &&
  session.feedback.map((item, idx) => (
    <div key={idx} className="feedback-item">
      <span className="feedback-icon">💡</span>
      <span className="feedback-text">{item}</span>
    </div>
))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="detail-section">
            <h3>Areas for Improvement</h3>
            <div className="recommendations-list">
              {Array.isArray(session.suggestions) &&
  session.suggestions.map((item, idx) => (
    <div key={idx} className="recommendation-item">
      <span className="recommendation-icon">📌</span>
      <span className="recommendation-text">{item}</span>
    </div>
))}
            </div>
          </div>

          {/* Action Button */}
          <div className="detail-section">
            <button className="practice-again-button">
              Practice This Session Again
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

const SessionHistory = () => {
  const navigate = useNavigate();
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionsData, setSessionsData] = useState([]);

useEffect(() => {
  const storedUser = localStorage.getItem("user");

  if (!storedUser) {
    console.error("User not logged in");
    return;
  }

  const user = JSON.parse(storedUser);

  fetch(`http://localhost:8000/sessions/${user.id}`)
    .then(res => res.json())
    .then(data => setSessionsData(data))
    .catch(err => console.error(err));

}, []);

  return (
    <div className="session-history-page">
      {/* Header */}
      <div className="history-page-header">
        <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>
          ← Back to Dashboard
        </button>
        <div className="header-content">
          <h1>Sessions History</h1>
          <p className="header-subtitle">Review and analyze all your speaking practice sessions with detailed <br />AI-powered feedback</p>
        </div>
      </div>

      {/* Stats Bar */}
      <div className="history-stats">
        <div className="history-stat">
          <span className="stat-label">Total Sessions</span>
          <span className="stat-value">{sessionsData.length}</span>
        </div>
        <div className="history-stat">
          <span className="stat-label">Average Score</span>
<span className="stat-value">
  {sessionsData.length
    ? (sessionsData.reduce((sum, s) => sum + s.score, 0) / sessionsData.length).toFixed(1)
    : "0"}
</span>        </div>
        <div className="history-stat">
          <span className="stat-label">Best Score</span>
<span className="stat-value">
  {sessionsData.length
    ? Math.max(...sessionsData.map(s => s.score)).toFixed(1)
    : "0"}
</span>        </div>
      </div>

      {/* Sessions List */}
      <div className="sessions-history-container">
        <div className="sessions-list">
          {sessionsData.length > 0 ? (
            sessionsData.map((session) => (
              <div 
                key={session.id} 
                className="session-list-item"
                onClick={() => setSelectedSession(session)}
                role="button"
                tabIndex={0}
              >
                {/* Video Thumbnail */}
                <div className="session-thumbnail-wrapper">
                  <video
                    className="session-thumbnail"
                    src={`http://localhost:8000/videos/${session.video_path.split("/").pop()}`}
                    preload="metadata"
                  >
                    Your browser does not support the video tag.
                  </video>
                  <div className="thumbnail-overlay">
                    <span className="play-icon">▶</span>
                  </div>
                </div>

                {/* Session Info */}
                <div className="session-list-content">
                  <div className="session-header-info">
                    <h4 className="session-title">{session.title}</h4>
                    <span className="session-type-badge">{session.type}</span>
                  </div>
                  <p className="session-meta">{session.date} • {session.duration}</p>
                  <p className="session-status">Status: <span className="status-text">{session.status}</span></p>
                </div>

                {/* Session Stats */}
                <div className="session-list-stats">
                  <div className="score-container">
                    <span className={`score-badge ${session.score >= 8.5 ? 'excellent' : session.score >= 8 ? 'very-good' : 'good'}`}>
                      {session.score.toFixed(1)}<span className="score-max">/10</span>
                    </span>
                    <p className="score-label">Overall Score</p>
                  </div>
                  <div className="action-indicator">
                    <span className="view-details">View Details</span>
                    <span className="arrow-icon">→</span>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="sessions-note">
              <p>No sessions recorded yet. <strong>Start a new practice session to get AI feedback!</strong></p>
            </div>
          )}
        </div>
      </div>

      {/* Session Detail Modal */}
      {selectedSession && (
        <SessionDetailModal session={selectedSession} onClose={() => setSelectedSession(null)} />
      )}
    </div>
  );
};

export default SessionHistory;
