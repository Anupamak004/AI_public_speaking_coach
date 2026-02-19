import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

const sessionsData = [
  {
    id: 1,
    title: "Session 12: Advanced Storytelling",
    date: "Feb 15, 2026",
    score: 9.1,
    duration: "8:45 min",
    status: "Completed",
    type: "Advanced Storytelling",
    metrics: {
      clarity: 9.0,
      pacing: 8.8,
      confidence: 9.3,
      engagement: 8.9,
      fillerWords: 2,
      eyeContact: 8.5
    },
    feedback: [
      "Excellent narrative flow and emotional delivery",
      "Great pauses for emphasis and audience engagement",
      "Minor filler word usage near the beginning",
      "Strong conclusion with memorable takeaway"
    ],
    improvements: [
      "Continue practicing storytelling techniques",
      "Maintain this level of confidence and presence",
      "Work slightly on minimizing filler words"
    ]
  },
  {
    id: 2,
    title: "Session 11: Product Pitch",
    date: "Feb 12, 2026",
    score: 8.7,
    duration: "7:30 min",
    status: "Completed",
    type: "Product Pitch",
    metrics: {
      clarity: 8.9,
      pacing: 8.5,
      confidence: 8.4,
      engagement: 8.6,
      fillerWords: 4,
      eyeContact: 8.1
    },
    feedback: [
      "Clear value proposition presented effectively",
      "Good product feature explanation",
      "Pacing could be slightly faster in some sections",
      "Eye contact improved significantly"
    ],
    improvements: [
      "Practice tighter pacing for product details",
      "Enhance engagement through more interactive elements",
      "Continue working on eye contact consistency"
    ]
  },
  {
    id: 3,
    title: "Session 10: Public Speaking Basics",
    date: "Feb 10, 2026",
    score: 8.3,
    duration: "9:15 min",
    status: "Completed",
    type: "Public Speaking Basics",
    metrics: {
      clarity: 8.2,
      pacing: 7.9,
      confidence: 8.5,
      engagement: 8.1,
      fillerWords: 5,
      eyeContact: 7.8
    },
    feedback: [
      "Solid foundational delivery",
      "Good use of body language",
      "Some improvement needed in pacing consistency",
      "Strong closing statement"
    ],
    improvements: [
      "Work on reducing filler words (um, uh, etc.)",
      "Practice varied pacing techniques",
      "Build more direct eye contact with audience"
    ]
  },
  {
    id: 4,
    title: "Session 9: Persuasion Techniques",
    date: "Feb 08, 2026",
    score: 8.5,
    duration: "8:00 min",
    status: "Completed",
    type: "Persuasion Techniques",
    metrics: {
      clarity: 8.6,
      pacing: 8.3,
      confidence: 8.4,
      engagement: 8.7,
      fillerWords: 6,
      eyeContact: 8.0
    },
    feedback: [
      "Effective use of persuasive language",
      "Good argument structure and flow",
      "Moderate filler word usage",
      "Strong audience engagement techniques"
    ],
    improvements: [
      "Reduce filler words for more professional delivery",
      "Enhance body language gestures",
      "Practice more natural pauses between key points"
    ]
  },
  {
    id: 5,
    title: "Session 8: Introduction Skills",
    date: "Feb 05, 2026",
    score: 8.1,
    duration: "7:45 min",
    status: "Completed",
    type: "Introduction Skills",
    metrics: {
      clarity: 8.0,
      pacing: 7.8,
      confidence: 8.2,
      engagement: 8.1,
      fillerWords: 7,
      eyeContact: 7.6
    },
    feedback: [
      "Good opening hook",
      "Clear introduction of main points",
      "Pacing needs some work",
      "Decent engagement level"
    ],
    improvements: [
      "Work on stronger opening statements",
      "Practice more controlled pacing",
      "Increase eye contact frequency"
    ]
  },
  {
    id: 6,
    title: "Session 7: Emotional Intelligence",
    date: "Feb 03, 2026",
    score: 8.2,
    duration: "8:30 min",
    status: "Completed",
    type: "Emotional Intelligence",
    metrics: {
      clarity: 8.3,
      pacing: 8.0,
      confidence: 8.4,
      engagement: 8.2,
      fillerWords: 5,
      eyeContact: 8.1
    },
    feedback: [
      "Good emotional connection with audience",
      "Effective tone modulation",
      "Consistent voice control",
      "Strong rapport building"
    ],
    improvements: [
      "Practice more varied vocal inflections",
      "Work on longer pauses for impact",
      "Continue building emotional narratives"
    ]
  },
  {
    id: 7,
    title: "Session 6: Audience Engagement",
    date: "Jan 31, 2026",
    score: 8.0,
    duration: "7:50 min",
    status: "Completed",
    type: "Audience Engagement",
    metrics: {
      clarity: 8.1,
      pacing: 7.9,
      confidence: 8.0,
      engagement: 8.5,
      fillerWords: 6,
      eyeContact: 7.9
    },
    feedback: [
      "Excellent interactive elements",
      "Good use of questions",
      "Audience attention maintained throughout",
      "Engaging closing Q&A session"
    ],
    improvements: [
      "Include more open-ended questions",
      "Practice anticipating audience reactions",
      "Develop more interactive techniques"
    ]
  },
  {
    id: 8,
    title: "Session 5: Voice Control",
    date: "Jan 28, 2026",
    score: 7.8,
    duration: "8:15 min",
    status: "Completed",
    type: "Voice Control",
    metrics: {
      clarity: 7.9,
      pacing: 7.7,
      confidence: 7.8,
      engagement: 7.8,
      fillerWords: 8,
      eyeContact: 7.6
    },
    feedback: [
      "Voice projection is improving",
      "Pace needs more work",
      "Good breathing techniques",
      "Moderate filler word usage"
    ],
    improvements: [
      "Practice power notes for emphasis",
      "Work on pitch variation",
      "Develop more breathing exercises"
    ]
  }
];

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
              {session.feedback.map((item, idx) => (
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
              {session.improvements.map((item, idx) => (
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

  return (
    <div className="session-history-page">
      {/* Header */}
      <div className="history-page-header">
        <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>
          ← Back to Dashboard
        </button>
        <div className="header-content">
          <h1>Sessions History</h1>
          <p className="header-subtitle">Review and analyze all your speaking practice sessions with detailed AI-powered feedback</p>
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
          <span className="stat-value">{(sessionsData.reduce((sum, s) => sum + s.score, 0) / sessionsData.length).toFixed(1)}</span>
        </div>
        <div className="history-stat">
          <span className="stat-label">Best Score</span>
          <span className="stat-value">{Math.max(...sessionsData.map(s => s.score)).toFixed(1)}</span>
        </div>
      </div>

      {/* Sessions List */}
      <div className="sessions-history-container">
        <div className="sessions-list">
          {sessionsData.map((session) => (
            <div 
              key={session.id} 
              className="session-list-item"
              onClick={() => setSelectedSession(session)}
              role="button"
              tabIndex={0}
            >
              <div className="session-list-left">
                <div className="session-number">#{session.id}</div>
                <div className="session-info">
                  <h4>{session.title}</h4>
                  <p>{session.date} • {session.duration}</p>
                </div>
              </div>
              <div className="session-list-middle">
                <span className="session-type-badge">{session.type}</span>
              </div>
              <div className="session-list-right">
                <div className="session-score-display">
                  <span className={`score-badge ${session.score >= 8.5 ? 'excellent' : session.score >= 8 ? 'very-good' : 'good'}`}>
                    {session.score.toFixed(1)}/10
                  </span>
                </div>
                <span className="view-details">View Details →</span>
              </div>
            </div>
          ))}
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
