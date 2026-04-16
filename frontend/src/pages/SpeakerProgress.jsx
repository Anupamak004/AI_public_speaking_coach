import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

// --- Score Circle Component ---
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

// --- Main Component ---
const SpeakerProgress = () => {
  const navigate = useNavigate();
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSessions = async () => {
      try {
        const user = JSON.parse(localStorage.getItem("user"));
        const user_id = user?.id;

        if (!user_id) {
          setSessions([]);
          return;
        }

        const res = await fetch(`http://127.0.0.1:8000/sessions/${user_id}`);
        const data = await res.json();
        setSessions(Array.isArray(data) ? data : []);
      } catch (err) {
        console.error(err);
        setSessions([]);
      } finally {
        setLoading(false);
      }
    };

    fetchSessions();
  }, []);

  if (loading)
    return <h2 style={{ padding: "20px" }}>Loading your progress...</h2>;

  // --- Stats ---
  const totalSessions = sessions.length;
  const scores = sessions.map((s) => s.metrics?.Confidence || 0);
  const averageScore = scores.length > 0 ? scores.reduce((a, b) => a + b, 0) / scores.length : 0;
  const bestScore = scores.length > 0 ? Math.max(...scores) : 0;

  const sortedSessions = [...sessions].sort(
    (a, b) => new Date(b.created_at) - new Date(a.created_at)
  );

  const latestSession = sortedSessions[0] || null;
  const previousSession = sortedSessions[1] || null;

  // --- Metrics with growth ---
  // --- Metrics with average + correct growth logic ---
const metricsData = latestSession?.metrics
  ? Object.keys(latestSession.metrics).map((key) => {
      const values = sessions.map((s) => s.metrics?.[key] ?? 0);

      // ✅ Average score
      const avgScore =
        values.length > 0
          ? values.reduce((a, b) => a + b, 0) / values.length
          : 0;

      // ✅ Highest score
      const maxScore = Math.max(...values);

      let growth;

      // ✅ Special case: Nervousness (lower is better)
      if (key.toLowerCase() === "nervousness") {
        growth = maxScore - avgScore;  // lower = improvement
      } else {
        growth = avgScore - maxScore;  // normal metrics
      }

      return {
        name: key.charAt(0).toUpperCase() + key.slice(1),
        score: avgScore, // ✅ keep original value
        growth,
      };
    })
  : [];

  // --- Trend chart ---
  const scoresTrend = sessions
    .slice()
    .reverse()
    .map((s, idx) => ({ session: `S${idx + 1}`, score: s.metrics?.Confidence || 0 }));

  const minScore = 0;
  const maxScore = 10;
  const scoreRange = maxScore - minScore;

  // --- Feedback ---
  const feedbackList = Array.isArray(latestSession?.feedback)
    ? latestSession.feedback
    : latestSession?.feedback
    ? [latestSession.feedback]
    : [];

  const generateChartMarkings = () => {
    const gridLines = [];
    const yAxisLabels = [];
    const xAxisLabels = [];

    for (let i = 0; i <= 10; i++) {
      const yPos = 270 - (i / 10) * 180;
      gridLines.push(
        <line key={`grid-${i}`} x1="60" y1={yPos} x2="950" y2={yPos} stroke="#e5e7eb" strokeWidth="1" strokeDasharray="4,4" />
      );
      yAxisLabels.push(
        <text key={`y-label-${i}`} x="45" y={yPos + 5} textAnchor="end" fontSize="12" fill="#6b7280" fontWeight="500">{i}</text>
      );
    }

    scoresTrend.forEach((item, idx) => {
      const x = 60 + idx * 70;
      xAxisLabels.push(
        <text key={`x-label-${idx}`} x={x} y="290" textAnchor="middle" fontSize="12" fill="#6b7280" fontWeight="500">
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
        <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>
          ← Back to Dashboard
        </button>
        <div className="progress-header-content">
          <h1>Speaker Progress Dashboard</h1>
          <p className="header-subtitle">Track your speaking improvement with detailed analytics</p>
        </div>
      </div>

      {/* Stats */}
      <div className="stats-grid-4">
        <div className="stat-card-primary">
          <h3>Total Sessions</h3>
          <p className="stat-value">{totalSessions}</p>
          <p className="stat-subtext">practice sessions completed</p>
        </div>

        <div className="stat-card-primary">
          <h3>Average Score</h3>
          <p className="stat-value">{averageScore.toFixed(1)}</p>
          <p className="stat-subtext">out of 10</p>
        </div>

        <div className="stat-card-primary">
          <h3>Best Score</h3>
          <p className="stat-value">{bestScore.toFixed(1)}</p>
          <p className="stat-subtext">your peak performance</p>
        </div>

        <div className="stat-card-primary">
          <h3>Latest Score</h3>
          <p className="stat-value">{latestSession ? (latestSession.metrics?.Confidence || 0).toFixed(1) : "-"}</p>
          <p className="stat-subtext">most recent session</p>
        </div>
      </div>

      {/* Metrics */}
      <section className="performance-section">
        <h2>Performance Metrics</h2>
        <div className="metrics-grid">
          {metricsData.length > 0 ? metricsData.map((metric, idx) => (
            <div key={idx} className="metric-card">
              <ScoreCircle score={metric.score} metric={metric.name} />
              <p className={`metric-growth ${metric.growth > 0 ? "positive" : metric.growth < 0 ? "negative" : "neutral"}`}>
                {metric.growth > 0 && "↑"}
                {metric.growth < 0 && "↓"}
                {metric.growth === 0 && "→"} {Math.abs(metric.growth).toFixed(1)}
              </p>
            </div>
          )) : <p>No metrics available yet. Complete a session to see details.</p>}
        </div>
      </section>

      {/* Trend Chart */}
      <section className="trend-section">
        <h2>Score Progression</h2>
        <div className="chart-container">
          {scoresTrend.length > 0 ? (
            <svg viewBox="0 0 1000 350" className="trend-chart">
              {gridLines}
              {yAxisLabels}
              {xAxisLabels}
              <line x1="60" y1="50" x2="60" y2="270" stroke="#333" strokeWidth="2" />
              <line x1="60" y1="270" x2="950" y2="270" stroke="#333" strokeWidth="2" />
              <defs>
                <linearGradient id="gradientLine" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#4f46e5" />
                  <stop offset="100%" stopColor="#667eea" />
                </linearGradient>
              </defs>
              <polyline
                points={scoresTrend.map((item, idx) => {
                  const x = 60 + idx * 70;
                  const y = 270 - ((item.score - minScore) / scoreRange) * 180;
                  return `${x},${y}`;
                }).join(" ")}
                fill="none"
                stroke="url(#gradientLine)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              {scoresTrend.map((item, idx) => {
                const x = 60 + idx * 70;
                const y = 270 - ((item.score - minScore) / scoreRange) * 180;
                return (
                  <g key={idx}>
                    <circle cx={x} cy={y} r="6" fill="white" stroke="#4f46e5" strokeWidth="2" />
                    <circle cx={x} cy={y} r="3" fill="#4f46e5" />
                    <text x={x} y={y - 15} textAnchor="middle" fontSize="12" fill="#4f46e5" fontWeight="600">{Math.round(item.score)}</text>
                    <title>{`${item.session}: ${Math.round(item.score)}/10`}</title>
                  </g>
                );
              })}
            </svg>
          ) : <p>No session data available. Complete a session to see your progress.</p>}
        </div>
      </section>

      {/* Feedback */}
      <section className="feedback-section">
  <div className="feedback-header">
    <h2>💡 AI Feedback Insights</h2>
    <p>Your latest personalized suggestions</p>
  </div>

  <div className="feedback-container">
    {feedbackList.length > 0 ? feedbackList.map((f, idx) => (
      <div key={idx} className="feedback-card">
        
        <div className="feedback-left">
          <div className="feedback-badge">#{idx + 1}</div>
        </div>

        <div className="feedback-body">
          {typeof f === "object" ? Object.entries(f).map(([k, v], i) => (
            <div key={i} className="feedback-row">
              <span className="feedback-key">{k}</span>
              <span className="feedback-value">{v}</span>
            </div>
          )) : (
            <p className="feedback-text">{f}</p>
          )}
        </div>

      </div>
    )) : (
      <div className="no-feedback">
        <p>No feedback yet 🚀</p>
        <span>Complete a session to unlock AI suggestions</span>
      </div>
    )}
  </div>
</section>
    </div>
  );
};

export default SpeakerProgress;