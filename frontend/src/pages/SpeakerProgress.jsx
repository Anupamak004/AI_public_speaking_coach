import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

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

  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  // ✅ Fetch sessions (FIXED)
  useEffect(() => {
    const fetchSessions = async () => {
      try {
        // 🔥 GET user_id from stored "user"
        const user = JSON.parse(localStorage.getItem("user"));
        const user_id = user?.id;

        console.log("USER ID:", user_id); // debug

        if (!user_id) {
          console.error("No user_id found");
          setSessions([]);
          return;
        }

        const res = await fetch(`http://127.0.0.1:8000/sessions/${user_id}`);
        const data = await res.json();

        // ✅ ensure array
        if (Array.isArray(data)) {
          setSessions(data);
        } else {
          console.error("Unexpected response:", data);
          setSessions([]);
        }
      } catch (err) {
        console.error("Error fetching sessions:", err);
        setSessions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, []);

  // ✅ Loading
  if (loading) return <h2 style={{ padding: "20px" }}>Loading...</h2>;

  // ✅ Safe calculations
  const totalSessions = Array.isArray(sessions) ? sessions.length : 0;

  const scores = Array.isArray(sessions)
    ? sessions.map((s) => s.score || 0)
    : [];

  const averageScore =
    scores.length > 0
      ? scores.reduce((a, b) => a + b, 0) / scores.length
      : 0;

  const bestScore = scores.length > 0 ? Math.max(...scores) : 0;

  const scoresTrend = Array.isArray(sessions)
    ? sessions
        .slice()
        .reverse()
        .map((s, index) => ({
          session: `S${index + 1}`,
          score: s.score || 0,
        }))
    : [];

  const latestSession =
    Array.isArray(sessions) && sessions.length > 0 ? sessions[0] : null;

  const metricsData =
    latestSession && latestSession.metrics
      ? Object.entries(latestSession.metrics).map(([key, value]) => ({
          name: key.charAt(0).toUpperCase() + key.slice(1),
          score: value,
        }))
      : [];

  // ✅ Chart safe - Use fixed 0-10 scale
  const maxScore = 10;
  const minScore = 0;
  const scoreRange = 10;

  const feedbackList = Array.isArray(latestSession?.feedback)
  ? latestSession.feedback
  : latestSession?.feedback
  ? [latestSession.feedback]
  : [];

  // Helper to generate grid lines and axis labels
  const generateChartMarkings = () => {
    const markings = [];
    const gridLines = [];
    const yAxisLabels = [];
    const xAxisLabels = [];

    // Y-axis grid lines and labels (10-point scale)
    for (let i = 0; i <= 10; i++) {
      const yPos = 270 - (i / 10) * 180;
      gridLines.push(
        <line
          key={`grid-${i}`}
          x1="60"
          y1={yPos}
          x2="950"
          y2={yPos}
          stroke="#e5e7eb"
          strokeWidth="1"
          strokeDasharray="4,4"
        />
      );
      yAxisLabels.push(
        <text
          key={`y-label-${i}`}
          x="45"
          y={yPos + 5}
          textAnchor="end"
          fontSize="12"
          fill="#6b7280"
          fontWeight="500"
        >
          {i}
        </text>
      );
    }

    // X-axis labels
    scoresTrend.forEach((item, idx) => {
      const x = 60 + idx * 70;
      xAxisLabels.push(
        <text
          key={`x-label-${idx}`}
          x={x}
          y="290"
          textAnchor="middle"
          fontSize="12"
          fill="#6b7280"
          fontWeight="500"
        >
          {item.session}
        </text>
      );
    });

    return { gridLines, yAxisLabels, xAxisLabels };
  };

  const { gridLines, yAxisLabels, xAxisLabels } = generateChartMarkings();

  return (
    <div className="speaker-progress-page">
      {/* Header */}
      <div className="progress-header">
        <button
          className="back-to-dashboard"
          onClick={() => navigate("/dashboard")}
        >
          ← Back to Dashboard
        </button>

        <div className="progress-header-content">
          <h1>Speaker Progress Dashboard</h1>
          <p className="header-subtitle">
            Track your speaking improvement with detailed analytics
          </p>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid-4">
        <div className="stat-card-primary">
          <div className="stat-content">
            <h3>Total Sessions</h3>
            <p className="stat-value">{totalSessions}</p>
            <p className="stat-subtext">practice sessions completed</p>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-content">
            <h3>Average Score</h3>
            <p className="stat-value">{averageScore.toFixed(1)}</p>
            <p className="stat-subtext">out of 10</p>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-content">
            <h3>Best Score</h3>
            <p className="stat-value">{bestScore.toFixed(1)}</p>
            <p className="stat-subtext">your peak performance</p>
          </div>
        </div>

        <div className="stat-card-primary">
          <div className="stat-content">
            <h3>Latest Score</h3>
            <p className="stat-value">
              {latestSession ? latestSession.score.toFixed(1) : "-"}
            </p>
            <p className="stat-subtext">most recent session</p>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <section className="performance-section">
        <div className="section-header">
          <h2>Performance Metrics</h2>
          <p className="section-description">
            Detailed breakdown of your speaking abilities
          </p>
        </div>

        <div className="metrics-grid">
          {metricsData.length > 0 ? (
            metricsData.map((metric, idx) => (
              <div key={idx} className="metric-card">
                <ScoreCircle score={metric.score} metric={metric.name} />
                <p className="metric-description">
                  {metric.name} performance
                </p>
              </div>
            ))
          ) : (
            <p className="no-data-message">No metrics available yet. Complete a session to see detailed metrics.</p>
          )}
        </div>
      </section>

      {/* Chart */}
      <section className="trend-section">
        <div className="section-header">
          <h2>Score Progression</h2>
          <p className="section-description">
            Your performance trend over time
          </p>
        </div>

        <div className="chart-container">
          {scoresTrend.length > 0 ? (
            <svg viewBox="0 0 1000 350" className="trend-chart">
              {/* Title */}
              <text
                x="500"
                y="25"
                textAnchor="middle"
                fontSize="14"
                fill="#1a365d"
                fontWeight="600"
              >
                Performance Over Time
              </text>

              {/* Y-axis label */}
              <text
                x="20"
                y="180"
                textAnchor="middle"
                fontSize="12"
                fill="#6b7280"
                fontWeight="500"
              >
                Score
              </text>

              {/* X-axis label */}
              <text
                x="500"
                y="330"
                textAnchor="middle"
                fontSize="12"
                fill="#6b7280"
                fontWeight="500"
              >
                Sessions
              </text>

              {/* Grid lines */}
              {gridLines}

              {/* Y-axis */}
              <line x1="60" y1="50" x2="60" y2="270" stroke="#333" strokeWidth="2" />

              {/* X-axis */}
              <line x1="60" y1="270" x2="950" y2="270" stroke="#333" strokeWidth="2" />

              {/* Y-axis labels */}
              {yAxisLabels}

              {/* X-axis labels */}
              {xAxisLabels}

              {/* Data line with gradient */}
              <defs>
                <linearGradient id="gradientLine" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#4f46e5" />
                  <stop offset="100%" stopColor="#667eea" />
                </linearGradient>
              </defs>

              {/* Polyline chart */}
              <polyline
                points={scoresTrend
                  .map((item, idx) => {
                    const x = 60 + idx * 70;
                    const y =
                      270 - ((item.score - minScore) / scoreRange) * 180;
                    return `${x},${y}`;
                  })
                  .join(" ")}
                fill="none"
                stroke="url(#gradientLine)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />

              {/* Data points */}
              {scoresTrend.map((item, idx) => {
                const x = 60 + idx * 70;
                const y =
                  270 - ((item.score - minScore) / scoreRange) * 180;

                return (
                  <g key={idx}>
                    <circle cx={x} cy={y} r="6" fill="white" stroke="#4f46e5" strokeWidth="2" />
                    <circle cx={x} cy={y} r="3" fill="#4f46e5" />
                    {/* Score label above point */}
                    <text
                      x={x}
                      y={y - 15}
                      textAnchor="middle"
                      fontSize="12"
                      fill="#4f46e5"
                      fontWeight="600"
                    >
                      {Math.round(item.score)}
                    </text>
                    {/* Tooltips on hover */}
                    <title>{`${item.session}: ${Math.round(item.score)}/10`}</title>
                  </g>
                );
              })}
            </svg>
          ) : (
            <p className="no-data-message">No session data available. Complete a session to see your progress.</p>
          )}
        </div>
      </section>

      {/* Feedback */}
      <section className="improvements-section">
        <div className="section-header">
          <h2>Latest Feedback</h2>
          <p className="section-description">
            Personalized recommendations from your most recent session
          </p>
        </div>

        <div className="improvements-list">
          {feedbackList.length > 0 ? (
            feedbackList.map((f, idx) => (
              <div key={idx} className="improvement-item">
                <div className="improvement-icon">✓</div>
                <div className="improvement-content">
                  {typeof f === "object" ? (
                    <div>
                      {Object.entries(f).map(([key, value], i) => (
                        <div key={i} className="feedback-entry">
                          <strong className="feedback-label">{key}:</strong>
                          <span className="feedback-value">{value}</span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p>{f}</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <p className="no-data-message">No feedback available. Complete a session to receive recommendations.</p>
          )}
        </div>
      </section>
    </div>
  );
};

export default SpeakerProgress;