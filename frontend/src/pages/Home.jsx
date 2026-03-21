import React from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { useState } from "react";
import { useEffect } from "react";
import "../styles/app.css";

const Home = () => {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const scrollToLogin = () => {
    const el = document.getElementById("login-section");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };
  const handleLogin = async (e) => {
  e.preventDefault();

  try {
    const res = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);

    // ✅ Store logged-in user
    localStorage.setItem(
      "user",
      JSON.stringify({ id: data.user_id })
    );

    navigate("/dashboard");

  } catch (err) {
    alert(err.message);
  }
};

  const location = useLocation();

useEffect(() => {
  if (location.state?.scrollTo) {
    const el = document.getElementById(location.state.scrollTo);
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }

    // ✅ CLEAR state so refresh doesn't scroll again
    navigate(location.pathname, { replace: true, state: {} });
  }
}, [location, navigate]);




  return (
    <>
      {/* NAVBAR */}
      <div className="navbar">
        <div className="nav-container">
          <div className="logo">
            <span>AI Speaking Coach</span>
          </div>
          <div className="nav-links">
            <a href="#features" className="nav-link">Features</a>
            <a href="#testimonials" className="nav-link">Testimonials</a>
            <a href="/register" className="nav-link cta-button">Get Started</a>
          </div>
        </div>
      </div>

      {/* HERO */}
      <div className="hero">
        <div className="hero-content">
          <h1>Master Public Speaking with AI</h1>

          <div className="hero-subtitle">
            Transform your presentation skills with our advanced AI-powered platform.
            <br />
            Get real-time feedback, personalized coaching, and data-driven insights.
          </div>

          <div className="hero-features">
            <div className="feature-item"> AI Analysis</div>
            <div className="feature-item"> Real-time Feedback</div>
            <div className="feature-item"> Progress Tracking</div>
          </div>

          <div className="hero-buttons">
            <button className="btn-primary" onClick={scrollToLogin}>
              Start Practice
            </button>
            <button className="btn-secondary">Watch Demo</button>
          </div>
        </div>
      </div>

      {/* STATS */}
      <div className="stats">
        <div className="stats-container">
          <div className="stat-item">
            <div className="stat-number">10K+</div>
            <div className="stat-label">Active Users</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">500K+</div>
            <div className="stat-label">Presentations Analyzed</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">95%</div>
            <div className="stat-label">Improvement Rate</div>
          </div>
          <div className="stat-item">
            <div className="stat-number">4.9★</div>
            <div className="stat-label">User Rating</div>
          </div>
        </div>
      </div>

      {/* FEATURES */}
<div id="features" className="features">
  <div className="features-container">
    <div className="section-header">
      <h2
        className="section-title"
        style={{
          fontSize: "2.5rem",
          fontWeight: 700,
          color: "#000000",
          marginBottom: "1rem",
        }}
      >
        Powerful Features for Professional Growth
      </h2>

      <div
        className="section-subtitle"
        style={{
          fontSize: "1.125rem",
          color: "#718096",
          maxWidth: "600px",
          margin: "0 auto",
          textAlign: "center",
        }}
      >
        Our AI-powered platform provides comprehensive analysis and personalized coaching
        to help you become a confident and effective public speaker.
      </div>
    </div>

    <div className="features-grid">
      <div className="feature-card">
        <div className="feature-icon">🧠</div>
        <h3 className="feature-title">Advanced AI Analysis</h3>
        <p className="feature-description">
          Our deep learning algorithms analyze speech patterns, facial expressions,
          body language, and vocal delivery in real-time for comprehensive feedback.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">📊</div>
        <h3 className="feature-title">Real-time Feedback</h3>
        <p className="feature-description">
          Get instant feedback on your performance with detailed metrics on pace,
          clarity, engagement, and confidence levels during your presentation.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">🎯</div>
        <h3 className="feature-title">Personalized Coaching</h3>
        <p className="feature-description">
          Receive tailored recommendations and practice exercises based on your
          unique strengths and areas for improvement.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">📈</div>
        <h3 className="feature-title">Progress Tracking</h3>
        <p className="feature-description">
          Monitor your improvement over time with detailed analytics, performance
          history, and achievement milestones.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">🎥</div>
        <h3 className="feature-title">Video Analysis</h3>
        <p className="feature-description">
          Upload presentation videos for detailed analysis of your delivery,
          visual aids usage, and audience engagement techniques.
        </p>
      </div>

      <div className="feature-card">
        <div className="feature-icon">📱</div>
        <h3 className="feature-title">Mobile Practice</h3>
        <p className="feature-description">
          Practice anywhere with our mobile app. Record sessions, get feedback,
          and track progress on the go.
        </p>
      </div>
    </div>
  </div>
</div>


      {/* TESTIMONIALS */}
<div id="testimonials" className="testimonials">
  <div className="testimonials-container">
    <div className="section-header">
      <h2 className="section-title">What Our Users Say</h2>

      <div
        className="section-subtitle"
        style={{
          fontSize: "1.125rem",
          color: "#718096",
          maxWidth: "100%",
          margin: "0 auto",
          textAlign: "center",
        }}
      >
        Join thousands of professionals who have transformed their public speaking skills
      </div>
    </div>

    <div className="testimonials-grid">
      <div className="testimonial-card">
        <p className="testimonial-text">
          "This AI coach completely transformed my presentation skills. The real-time feedback
          helped me identify and fix issues I never knew I had. My confidence has skyrocketed!"
        </p>

        <div className="testimonial-author">
          <div className="author-avatar">SM</div>
          <div className="author-info">
            <h4>Sarah Mitchell</h4>
            <p>Marketing Director</p>
          </div>
        </div>
      </div>

      <div className="testimonial-card">
        <p className="testimonial-text">
          "As someone who dreaded public speaking, this platform made practice enjoyable and
          effective. The personalized coaching feels like having a professional trainer available 24/7."
        </p>

        <div className="testimonial-author">
          <div className="author-avatar">JD</div>
          <div className="author-info">
            <h4>James Davis</h4>
            <p>Software Engineer</p>
          </div>
        </div>
      </div>

      <div className="testimonial-card">
        <p className="testimonial-text">
          "The analytics and progress tracking features are incredible. I can see exactly
          how I'm improving over time. This is a game-changer for professional development."
        </p>

        <div className="testimonial-author">
          <div className="author-avatar">LC</div>
          <div className="author-info">
            <h4>Lisa Chen</h4>
            <p>Sales Manager</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>


   {/* LOGIN SECTION */}
<section className="login-section" id="login-section">
        <div className="login-container">

          {/* ---------- LEFT : INTRO ---------- */}
          <div className="login-left">
            <div className="intro-box">
              <h1>
                 Speak Confidently.<br />
                Speak Smarter.
              </h1>

              <p>
                AI Public Speaking Coach helps you improve confidence,
                clarity, and delivery using real-time AI feedback on voice,
                expressions, and content.
              </p>

              <ul className="intro-list">
                <li>✓ AI-powered speech analysis</li>
                <li>✓ Real-time feedback & insights</li>
                <li>✓ Personalized improvement tips</li>
                <li>✓ Track progress over time</li>
              </ul>
            </div>
          </div>

          {/* ---------- RIGHT : LOGIN ---------- */}
          <div className="login-right">
            <form className="login-form" onSubmit={handleLogin}>
              <h2 className="login-title">Login to Your Account</h2>
              <p className="login-subtitle">
                Continue your speaking journey
              </p>

              <input
              type="email"
              placeholder="Email Address"
              className="input-field"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />

            <input
              type="password"
              placeholder="Password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />

              <button type="submit" className="btn-primary full-width">
                Login
              </button>
            </form>
          </div>

        </div>
      </section>



      {/* FOOTER */}
<div className="footer">
  <div className="footer-container">
    <div className="footer-section">
      <h3>AI Speaking Coach</h3>
      <p>
        Transform your public speaking skills with cutting-edge AI technology.
        Get personalized feedback and real-time analysis to become a confident presenter.
      </p>
    </div>

    <div className="footer-section">
      <h3>Product</h3>
      <ul className="footer-links">
        <li><a href="#">Features</a></li>
        <li><a href="#">Pricing</a></li>
        <li><a href="#">API</a></li>
        <li><a href="#">Integrations</a></li>
      </ul>
    </div>

    <div className="footer-section">
      <h3>Company</h3>
      <ul className="footer-links">
        <li><a href="#">About</a></li>
        <li><a href="#">Blog</a></li>
        <li><a href="#">Careers</a></li>
        <li><a href="#">Contact</a></li>
      </ul>
    </div>

    <div className="footer-section">
      <h3>Support</h3>
      <ul className="footer-links">
        <li><a href="#">Help Center</a></li>
        <li><a href="#">Documentation</a></li>
        <li><a href="#">Community</a></li>
        <li><a href="#">Status</a></li>
      </ul>
    </div>
  </div>

  <div className="footer-bottom">
    <p>© 2025 AI Public Speaking Coach. All rights reserved. | Final Year Project</p>
  </div>
</div>

    </>
  );
};

export default Home;
