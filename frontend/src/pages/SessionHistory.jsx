import React, { useState,useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

const SessionDetailModal = ({ session, sessionIndex, onClose }) => {
  if (!session) return null;

  // Get confidence score from metrics or use overall score
  const confidenceScore = session.metrics?.Confidence || session.score;
  
  // Function to get performance level
  const getPerformanceLevel = (score) => {
    if (score >= 8) return { level: "Excellent", class: "excellent" };
    if (score >= 6) return { level: "Good", class: "good" };
    if (score >= 4) return { level: "Fair", class: "fair" };
    return { level: "Needs Improvement", class: "poor" };
  };

  const performance = getPerformanceLevel(confidenceScore);

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="session-detail-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Session {sessionIndex}</h2>
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
            </div>
          </div>

          {/* Overall Score */}
          <div className="detail-section overall-score-detail">
            <h3>Overall Confidence Score</h3>
            <div className="overall-score-container">
              {/* Left Side: Score Display */}
              <div className="score-display-left">
                <div className="score-number-large">
                  {Math.round(confidenceScore)}
                  <span className="score-max-large">/10</span>
                </div>
                <div className={`score-performance-level-detail ${performance.class}`}>
                  {performance.level}
                </div>
              </div>

              {/* Right Side: Gauge Bar */}
              <div className="score-gauge-bar-detail">
                <div className="gauge-track-detail">
                  <div
                    className="gauge-fill-detail"
                    style={{
                      width: `${(confidenceScore / 10) * 100}%`,
                    }}
                  />
                </div>
                <div className="gauge-scale-detail">
                  <div className="gauge-label-detail">0</div>
                  <div className="gauge-label-detail">2.5</div>
                  <div className="gauge-label-detail">5</div>
                  <div className="gauge-label-detail">7.5</div>
                  <div className="gauge-label-detail">10</div>
                </div>
                <p className="score-description-detail">
                  Your confidence level demonstrates{" "}
                  <strong>
                    {performance.class === "excellent" && "outstanding performance"}
                    {performance.class === "good" && "strong proficiency"}
                    {performance.class === "fair" && "room for improvement"}
                    {performance.class === "poor" && "significant growth opportunity"}
                  </strong>
                </p>
              </div>
            </div>
          </div>

          {/* Detailed Metrics */}
          <div className="detail-section">
            <h3>Detailed Metrics Breakdown</h3>
            <div className="metrics-breakdown">
              {Object.entries(session.metrics).filter(([key]) => key !== 'Confidence').map(([key, value]) => (
                <div key={key} className="metric-row">
                  <div className="metric-left">
                    <span className="metric-label">{key.replace(/([A-Z])/g, ' $1').trim()}</span>
                    <span className="metric-score">{typeof value === 'number' ? Math.round(value) : value}</span>
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
  const [selectedSessionIndex, setSelectedSessionIndex] = useState(null);
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
    ? Math.round(sessionsData.reduce((sum, s) => sum + (s.metrics?.Confidence || s.score), 0) / sessionsData.length)
    : "0"}
</span>        </div>
        <div className="history-stat">
          <span className="stat-label">Best Score</span>
<span className="stat-value">
  {sessionsData.length
    ? Math.round(Math.max(...sessionsData.map(s => s.metrics?.Confidence || s.score)))
    : "0"}
</span>        </div>
      </div>

      {/* Sessions List */}
      <div className="sessions-history-container">
        <div className="sessions-list">
          {sessionsData.length > 0 ? (
            sessionsData.map((session, index) => (
              <div 
                key={session.id} 
                className="session-list-item"
                onClick={() => {
                  setSelectedSession(session);
                  setSelectedSessionIndex(index + 1);
                }}
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
                    <h4 className="session-title">{session.title}</h4>                  </div>
                  <p className="session-meta">{session.date} • {session.duration}</p>
                </div>

                {/* Session Stats */}
                <div className="session-list-stats">
                  <div className="score-container">
                    <span className={`score-badge ${(session.metrics?.Confidence || session.score) >= 8 ? 'excellent' : (session.metrics?.Confidence || session.score) >= 6 ? 'very-good' : 'good'}`}>
                      {Math.round(session.metrics?.Confidence || session.score)}<span className="score-max">/10</span>
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
        <SessionDetailModal session={selectedSession} sessionIndex={selectedSessionIndex} onClose={() => setSelectedSession(null)} />
      )}
    </div>
  );
};

export default SessionHistory;
