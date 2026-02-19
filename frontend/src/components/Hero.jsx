const Hero = () => {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>Master Public Speaking with AI</h1>

        <div className="hero-subtitle">
          Transform your presentation skills with our advanced AI-powered platform.
          <br />
          Get real-time feedback, personalized coaching, and data-driven insights.
        </div>

        <div className="hero-features">
          <div className="feature-item">🎯 AI Analysis</div>
          <div className="feature-item">📊 Real-time Feedback</div>
          <div className="feature-item">📈 Progress Tracking</div>
        </div>

        <div className="hero-buttons">
          <button
            className="btn-primary"
            onClick={() =>
              document.getElementById("login-section").scrollIntoView()
            }
          >
            Start Practice
          </button>
          <button className="btn-secondary">Watch Demo</button>
        </div>
      </div>
    </div>
  );
};

export default Hero;
