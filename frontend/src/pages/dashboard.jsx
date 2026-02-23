import { useState } from "react";
import "../styles/dashboard.css";

export default function Dashboard() {
  const [video, setVideo] = useState(null);
  const [videoFile, setVideoFile] = useState(null);
  const [analyzed, setAnalyzed] = useState(false);
  const [loading, setLoading] = useState(false);
  const [scores, setScores] = useState([]);
  const [feedback, setFeedback] = useState({});
  const [suggestions, setSuggestions] = useState([]);

  const handleAnalyze = async () => {
  if (!videoFile) return;

  setLoading(true);
  setAnalyzed(false);

  try {
    const formData = new FormData();
    formData.append("file", videoFile);

    const response = await fetch("http://localhost:8001/analyze", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    console.log("Backend response:", data);

    // ✅ SAFETY CHECK
    if (!data || !data.scores || !data.scores.scores) {
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
    setSuggestions(data.scores.suggestions || []);
    setAnalyzed(true);

  } catch (err) {
    console.error("Analysis failed:", err);
    alert("Failed to analyze video");
  } finally {
    setLoading(false);
  }
};

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

        {/* UPLOAD */}
        <div className="upload-preview-card">
          <h3>Upload Presentation</h3>

          <div className="video-preview-wrapper">
            {video ? (
              <>
                <video src={video} controls className="video-preview" />
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
                <span className="upload-icon">🎥</span>
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

            <h2
              style={{
                fontSize: "1.4rem",
                fontWeight: 700,
                marginBottom: "18px",
              }}
            >
              Performance Overview
            </h2>

            {/* SCORES GRID */}
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fit, minmax(160px, 1fr))",
                gap: "20px",
              }}
            >
              {scores.map((item) => (
                <div
                  key={item.label}
                  style={{
                    background: "white",
                    padding: "20px",
                    borderRadius: "12px",
                    textAlign: "center",
                  }}
                >
                  <div
                    style={{
                      fontSize: "28px",
                      fontWeight: 700,
                      color: "#4f46e5",
                    }}
                  >
                    {item.value}/10
                  </div>

                  <div style={{ marginTop: "6px", fontWeight: 600 }}>
                    {item.label}
                  </div>

                  {feedback[item.label] && (
                    <p
                      style={{
                        marginTop: "10px",
                        fontSize: "0.9rem",
                        color: "#6b7280",
                      }}
                    >
                      {feedback[item.label]}
                    </p>
                  )}
                </div>
              ))}
            </div>

            {/* SUGGESTIONS */}
            {suggestions.length > 0 && (
              <section style={{ marginTop: "40px" }}>
                <h2
                  style={{
                    fontSize: "1.4rem",
                    fontWeight: 700,
                    marginBottom: "16px",
                  }}
                >
                  Personalized Coaching Tips
                </h2>

                <div
                  style={{
                    background: "white",
                    padding: "20px",
                    borderRadius: "12px",
                  }}
                >
                  <ul
                    style={{
                      paddingLeft: "20px",
                      color: "#374151",
                    }}
                  >
                    {suggestions.map((tip, idx) => (
                      <li key={idx} style={{ marginBottom: "10px" }}>
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
