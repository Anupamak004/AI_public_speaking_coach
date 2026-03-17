import React from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

const speakerProgressData = {
  overview: {
    totalSessions: 12,
    averageScore: 8.4,
    bestScore: 9.5,
    improvementRate: 15,
    completionRate: 100
  },
  metrics: [
    {
      name: "Clarity",
      score: 8.8,
      trend: "↑ +2.1%",
      description: "Speech articulation and pronunciation"
    },
    {
      name: "Pacing",
      score: 8.2,
      trend: "↑ +1.8%",
      description: "Speech speed and rhythm control"
    },
    {
      name: "Confidence",
      score: 8.6,
      trend: "↑ +3.2%",
      description: "Delivery assertiveness and presence"
    },
    {
      name: "Engagement",
      score: 7.9,
      trend: "↑ +2.5%",
      description: "Audience connection and interaction"
    }
  ],
  improvements: [
    { text: "Reduced filler words by 35%", date: "Last 3 sessions" },
    { text: "Improved eye contact consistency", date: "Last 2 sessions" },
    { text: "Better emotion conveyance", date: "Last session" },
    { text: "Enhanced storytelling flow", date: "Last 2 sessions" },
    { text: "Clearer pronunciation in technical terms", date: "Consistent" }
  ],
  sessionHistory: [
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
    }
  ],
  scoresTrend: [
    { session: "S1", score: 6.8 },
    { session: "S2", score: 7.2 },
    { session: "S3", score: 7.5 },
    { session: "S4", score: 7.9 },
    { session: "S5", score: 8.1 },
    { session: "S6", score: 8.3 },
    { session: "S7", score: 8.2 },
    { session: "S8", score: 8.5 },
    { session: "S9", score: 8.4 },
    { session: "S10", score: 8.6 },
    { session: "S11", score: 8.7 },
    { session: "S12", score: 9.1 }
  ]
};

const ProgressBar = ({ percentage, label }) => {
  return (
    <div className="progress-bar-wrapper">
      <div className="progress-bar-label">
        <span>{label}</span>
        <span className="progress-percentage">{percentage}%</span>
      </div>
      <div className="progress-bar-container">
        <div 
          className="progress-bar-fill" 
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
    </div>
  );
};

const ScoreCircle = ({ score, metric }) => {
  const getColorClass = (score) => {
    if (score >= 9) return "excellent";
    if (score >= 8) return "very-good";
    if (score >= 7) return "good";
    return "fair";
  };

  return (
    <div className="score-circle-wrapper">
      <div className={`score-circle ${getColorClass(score)}`}>
        <span className="score-value">{score.toFixed(1)}</span>
        <span className="score-max">/10</span>
      </div>
      <p className="score-metric-name">{metric}</p>
    </div>
  );
};

const SpeakerProgress = () => {
  const navigate = useNavigate();
  const maxScore = Math.max(...speakerProgressData.scoresTrend.map(s => s.score));
  const minScore = Math.min(...speakerProgressData.scoresTrend.map(s => s.score));
  const scoreRange = maxScore - minScore;

  return (
    <div className="speaker-progress-page">
      {/* Header Section */}
      <div className="progress-header">
        <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>← Back to Dashboard</button>
        <div className="progress-header-content">
          <h1>Speaker Progress Dashboard</h1>
          <p className="header-subtitle">
            Track your journey to becoming a master speaker with detailed analytics and personalized feedback
          </p>
        </div>
      </div>

      {/* Top Stats Cards */}
      <div className="stats-grid-4">
        <div className="stat-card-primary">
          <div className="stat-icon">📊</div>
          <div className="stat-card-content">
            <h3>Total Sessions</h3>
            <p className="stat-value">{speakerProgressData.overview.totalSessions}</p>
            <span className="stat-subtext">Professional training sessions completed</span>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-icon">⭐</div>
          <div className="stat-card-content">
            <h3>Average Score</h3>
            <p className="stat-value">{speakerProgressData.overview.averageScore.toFixed(1)}</p>
            <span className="stat-subtext">Out of 10 throughout all sessions</span>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-icon">🏆</div>
          <div className="stat-card-content">
            <h3>Best Score</h3>
            <p className="stat-value">{speakerProgressData.overview.bestScore.toFixed(1)}</p>
            <span className="stat-subtext">Your highest achievement yet</span>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-icon">📈</div>
          <div className="stat-card-content">
            <h3>Improvement</h3>
            <p className="stat-value">+{speakerProgressData.overview.improvementRate}%</p>
            <span className="stat-subtext">Overall progress increase</span>
          </div>
        </div>
      </div>

      {/* Performance Metrics Section */}
      <section className="performance-section">
        <h2>Performance Metrics</h2>
        <p className="section-description">Detailed breakdown of your speaking skills across key dimensions</p>
        
        <div className="metrics-grid">
          {speakerProgressData.metrics.map((metric, idx) => (
            <div key={idx} className="metric-card">
              <div className="metric-header">
                <h3>{metric.name}</h3>
                <span className="metric-trend positive">{metric.trend}</span>
              </div>
              <ScoreCircle score={metric.score} metric={metric.name} />
              <p className="metric-description">{metric.description}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Score Trend Chart */}
      <section className="trend-section">
        <h2>Score Progression Over Time</h2>
        <p className="section-description">Your performance growth across all sessions</p>
        
        <div className="chart-container">
          <div className="chart-canvas">
            <svg viewBox="0 0 1000 300" className="trend-chart">
              {/* Grid Lines */}
              {[0, 2, 4, 6].map((i) => (
                <line 
                  key={`grid-${i}`}
                  x1="60" 
                  y1={50 + i * 40} 
                  x2="950" 
                  y2={50 + i * 40} 
                  stroke="#e5e7eb" 
                  strokeWidth="1"
                />
              ))}

              {/* Y-axis labels */}
              <text x="40" y="255" fontSize="12" fill="#666" textAnchor="end">6</text>
              <text x="40" y="215" fontSize="12" fill="#666" textAnchor="end">7</text>
              <text x="40" y="175" fontSize="12" fill="#666" textAnchor="end">8</text>
              <text x="40" y="135" fontSize="12" fill="#666" textAnchor="end">9</text>
              <text x="40" y="95" fontSize="12" fill="#666" textAnchor="end">10</text>

              {/* Axes */}
              <line x1="60" y1="50" x2="60" y2="270" stroke="#333" strokeWidth="2" />
              <line x1="60" y1="270" x2="950" y2="270" stroke="#333" strokeWidth="2" />

              {/* Plot line and points */}
              <polyline
                points={speakerProgressData.scoresTrend.map((item, idx) => {
                  const x = 60 + (idx * 70);
                  const normalizedScore = (item.score - minScore) / scoreRange;
                  const y = 270 - (normalizedScore * 180);
                  return `${x},${y}`;
                }).join(" ")}
                fill="none"
                stroke="#4f46e5"
                strokeWidth="3"
              />

              {/* Data points */}
              {speakerProgressData.scoresTrend.map((item, idx) => {
                const x = 60 + (idx * 70);
                const normalizedScore = (item.score - minScore) / scoreRange;
                const y = 270 - (normalizedScore * 180);
                return (
                  <circle 
                    key={`point-${idx}`}
                    cx={x} 
                    cy={y} 
                    r="5" 
                    fill="#4f46e5"
                  />
                );
              })}

              {/* X-axis labels */}
              {speakerProgressData.scoresTrend.map((item, idx) => (
                <text 
                  key={`label-${idx}`}
                  x={60 + (idx * 70)} 
                  y="295" 
                  fontSize="11" 
                  fill="#666" 
                  textAnchor="middle"
                >
                  {item.session}
                </text>
              ))}
            </svg>
          </div>
        </div>
      </section>

      {/* Improvements Section */}
      <section className="improvements-section">
        <h2>Key Improvements</h2>
        <p className="section-description">Notable progress areas identified during your sessions</p>
        
        <div className="improvements-list">
          {speakerProgressData.improvements.map((improvement, idx) => (
            <div key={idx} className="improvement-item">
              <div className="improvement-icon">✓</div>
              <div className="improvement-content">
                <p className="improvement-text">{improvement.text}</p>
                <span className="improvement-date">{improvement.date}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Next Steps Section */}
      <section className="next-steps-section">
        <h2>Recommended Next Steps</h2>
        <div className="next-steps-grid">
          <div className="next-step-card">
            <h3>🎯 Focus Area: Engagement</h3>
            <p>Work on improving audience engagement. Try incorporating more pauses and interactive elements in your presentations.</p>
          </div>
          <div className="next-step-card">
            <h3>📚 Master Advanced Techniques</h3>
            <p>You're doing great! Consider diving into advanced storytelling and emotional intelligence modules.</p>
          </div>
          <div className="next-step-card">
            <h3>🎬 Record Your Next Session</h3>
            <p>Schedule your next speaking session to continue building on your excellent progress.</p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default SpeakerProgress;