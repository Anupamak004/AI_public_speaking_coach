import { useState } from "react";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [video, setVideo] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [scores, setScores] = useState([]);
  const [feedback, setFeedback] = useState({});
  const [comprehensiveFeedback, setComprehensiveFeedback] = useState({});
  const [suggestions, setSuggestions] = useState([]);

  const handleAnalyze = async () => {
  if (!videoFile) return;

  setLoading(true);
  setAnalyzed(false);

  try {
    const user = JSON.parse(localStorage.getItem("user"));
    console.log("USER:", user);

const formData = new FormData();
formData.append("file", videoFile);
formData.append("user_id", String(user.id));

    const response = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

if (!response.ok) {
  console.error("Backend error:", data);
console.error("FULL ERROR:", JSON.stringify(data, null, 2));
throw new Error("Backend error");}

console.log("Backend response:", data);

    // ✅ SAFETY CHECK
    if (!data?.scores?.scores) {
  console.error("Unexpected structure:", data);
  throw new Error("Invalid backend response");
}

    // ✅ FIXED HERE
    const formattedScores = Object.entries(data.scores.scores).map(
      ([label, value]) => ({
        label,
        value,
      })
    );

    setScores(formattedScores);
    setFeedback(data.scores.feedback || {});
    setComprehensiveFeedback(data.scores.feedback || {});
    setSuggestions(data.scores.suggestions || []);
    setAnalyzed(true);


  } catch (err) {
    console.error("Analysis failed:", err);
    alert("Failed to analyze video");
  } finally {
    setLoading(false);
  }
};

  // ✅ EXTRACT CONFIDENCE AS MAIN SCORE
  const confidenceScore = scores.find(
    (item) => item.label.toLowerCase() === "confidence"
  );

  // ✅ REMOVE CONFIDENCE FROM SUB METRICS
  const otherScores = scores.filter(
    (item) => item.label.toLowerCase() !== "confidence"
  );

  return (
    <div className="dashboard" style={{ display: "flex", minHeight: "100vh" }}>
      {/* SIDEBAR */}
      <aside style={{ width: "240px", background: "#1a365d", color: "white", display: "flex", flexDirection: "column", padding: "32px 0" }}>
        <div style={{ fontSize: "2rem", fontWeight: "bold", textAlign: "center", marginBottom: "32px" }}>AI Speaking Coach</div>
        <nav style={{ flex: 1 }}>
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li style={{ padding: "16px 32px", background: "#23395d", borderRadius: "8px", marginBottom: "12px", fontWeight: 600 }}>Dashboard</li>
            <li style={{ padding: "16px 32px", cursor: "pointer"}} onClick={() => window.location.href = "/speaker-progress"}>Progress</li>
            <li style={{ padding: "16px 32px", cursor: "pointer"}} onClick={() => window.location.href = "/session-history"}>Session History</li>
            <li style={{ padding: "16px 32px", cursor: "pointer" }} onClick={() => window.location.href = "/settings"}>Settings</li>
          </ul>
        </nav>
        <button
          onClick={() => {
            localStorage.removeItem("user");
            window.location.href = "/";
          }}
          style={{
            margin: "0 16px 24px 16px",
            padding: "12px 20px",
            background: "#dc2626",
            color: "white",
            border: "none",
            borderRadius: "8px",
            fontWeight: 600,
            cursor: "pointer",
            transition: "background 0.3s ease",
          }}
          onMouseEnter={(e) => e.target.style.background = "#b91c1c"}
          onMouseLeave={(e) => e.target.style.background = "#dc2626"}
        >
          Logout
        </button>
        <div style={{ textAlign: "center", marginTop: "auto", fontSize: "0.95rem", opacity: 0.7 }}>© 2026 AI Speaking Coach</div>
      </aside>

      {/* MAIN */}
      <main
        style={{
          flex: 1,
          padding: "40px 48px",
          background: "#f8fafc",
        }}
      >
        {/* HEADER */}
        <div style={{ marginBottom: "32px" }}>
          <h1
            style={{
              fontSize: "2.2rem",
              fontWeight: 700,
              color: "#1a365d",
            }}
          >
            Dashboard Overview
          </h1>
          <p style={{ color: "#6b7280" }}>
            Upload a video to receive AI-powered speaking feedback.
          </p>
        </div>

        {/* HOME BUTTON */}
<button
  onClick={() => (window.location.href = "/")}
  style={{
    position: "absolute",
    top: "24px",
    right: "32px",
    background: "#4f46e5",
    color: "white",
    padding: "10px 18px",
    borderRadius: "10px",
    fontWeight: 600,
    border: "none",
    cursor: "pointer",
    boxShadow: "0 6px 16px rgba(0,0,0,0.15)",
    zIndex: 1000,
  }}
>
   Home
</button>

        {/* UPLOAD */}
        <div className="upload-preview-card">
          <h3>Upload Presentation</h3>

          <div className="video-preview-wrapper">
            {video ? (
              <>
                <video src={video} controls className="video-preview" />
                {!loading && !analyzed && (
                  <button
                    className="replace-btn"
                    onClick={() => {
                      setVideo(null);
                      setVideoFile(null);
                      setAnalyzed(false);
                    }}
                  >
                    Replace
                  </button>
                )}
              </>
            ) : (
              <label className="upload-label">
                <input
                  type="file"
                  accept="video/*"
                  hidden
                  onChange={(e) => {
                    const file = e.target.files[0];
                    if (!file) return;
                    setVideo(URL.createObjectURL(file));
                    setVideoFile(file);
                  }}
                />
                <span className="upload-icon"></span>
                <p className="muted-text">Click or drag video here</p>
              </label>
            )}
          </div>

          <button
            className="primary-btn"
            onClick={handleAnalyze}
            disabled={!videoFile || loading}
          >
            {loading ? "Analyzing..." : "Analyze Video"}
          </button>
        </div>

        {/* RESULTS */}
        {analyzed && (
          <section style={{ marginTop: "40px" }}>
            <div
              style={{
                background: "#ecfdf5",
                color: "#065f46",
                padding: "14px",
                borderRadius: "10px",
                marginBottom: "24px",
                fontWeight: 600,
              }}
            >
              ✅ Analysis completed successfully
            </div>

            {/* ✅ MAIN CONFIDENCE SCORE */}
            {confidenceScore && (
              <div className="overall-score-section">
                <h2>Overall Confidence Score</h2>
                <div className="circular-progress-container">
                  <svg className="circular-progress" viewBox="0 0 200 200">
                    {/* Background circle */}
                    <circle
                      cx="100"
                      cy="100"
                      r="90"
                      fill="none"
                      stroke="rgba(255, 255, 255, 0.2)"
                      strokeWidth="12"
                    />
                    {/* Progress circle */}
                    <circle
                      cx="100"
                      cy="100"
                      r="90"
                      fill="none"
                      stroke="url(#progressGradient)"
                      strokeWidth="12"
                      strokeDasharray={`${(confidenceScore.value / 10) * 565.5} 565.5`}
                      strokeLinecap="round"
                      className="progress-ring"
                    />
                    <defs>
                      <linearGradient id="progressGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                        <stop offset="0%" stopColor="#fbbf24" />
                        <stop offset="100%" stopColor="#f59e0b" />
                      </linearGradient>
                    </defs>
                  </svg>
                  <div className="score-display">
                    <div className="score-number">{confidenceScore.value}</div>
                    <div className="score-max">/10</div>
                  </div>
                </div>
                {feedback["Confidence"] && (
                  <p className="overall-score-feedback">
                    {feedback["Confidence"]}
                  </p>
                )}
              </div>
            )}

            {/* SUB SCORES */}
            {otherScores.length > 0 && (
              <div className="performance-breakdown">
                <h2 className="breakdown-header">
                  Performance Breakdown
                </h2>

                <div className="score-cards-grid">
                  {otherScores.map((item) => (
                    <div key={item.label} className="score-card">
                      <div className="score-card-number">
                        {item.value}
                        <span>/10</span>
                      </div>

                      <div className="score-card-label">
                        {item.label}
                      </div>

                      {feedback[item.label] && (
                        <p className="score-card-feedback">
                          {feedback[item.label]}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* FEEDBACK SECTIONS */}
            {comprehensiveFeedback.overall_feedback && (
              <section className="feedback-section">
                <h2 className="feedback-header">Overall Feedback</h2>
                <div className="feedback-content">
                  <p className="overall-feedback-text">{comprehensiveFeedback.overall_feedback}</p>
                </div>
              </section>
            )}

            {/* STRENGTHS */}
            {comprehensiveFeedback.strengths && comprehensiveFeedback.strengths.length > 0 && (
              <section className="feedback-section">
                <h2 className="feedback-header" style={{color: "#059669"}}>Strengths</h2>
                <div className="feedback-content">
                  <ul className="feedback-list">
                    {comprehensiveFeedback.strengths.map((strength, idx) => (
                      <li key={idx} className="strength-item">✓ {strength}</li>
                    ))}
                  </ul>
                </div>
              </section>
            )}

            {/* WEAKNESSES */}
            {comprehensiveFeedback.weaknesses && comprehensiveFeedback.weaknesses.length > 0 && (
              <section className="feedback-section">
                <h2 className="feedback-header" style={{color: "#dc2626"}}>Areas Needing Attention</h2>
                <div className="feedback-content">
                  <ul className="feedback-list">
                    {comprehensiveFeedback.weaknesses.map((weakness, idx) => (
                      <li key={idx} className="weakness-item">⚠ {weakness}</li>
                    ))}
                  </ul>
                </div>
              </section>
            )}

            {/* AREAS TO IMPROVE */}
            {comprehensiveFeedback.areas_to_improve && comprehensiveFeedback.areas_to_improve.length > 0 && (
              <section className="feedback-section">
                <h2 className="feedback-header" style={{color: "#2563eb"}}>Improvement Recommendations</h2>
                <div className="feedback-content">
                  <ul className="feedback-list">
                    {comprehensiveFeedback.areas_to_improve.map((area, idx) => (
                      <li key={idx} className="improvement-item">💡 {area}</li>
                    ))}
                  </ul>
                </div>
              </section>
            )}

            {/* LEGACY SUGGESTIONS - for backward compatibility */}
            {suggestions.length > 0 && !comprehensiveFeedback.areas_to_improve && (
              <section className="suggestions-section">
                <h2 className="suggestions-header">
                  Personalized Coaching Tips
                </h2>

                <div className="suggestions-container">
                  <ul className="suggestions-list">
                    {suggestions.map((tip, idx) => (
                      <li key={idx}>
                        {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              </section>
            )}
          </section>
        )}
      </main>
    </div>
  );
}