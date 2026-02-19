import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/dashboard.css";

export default function Settings() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("profile");
  const [formData, setFormData] = useState({
    fullName: "John Doe",
    email: "john@example.com",
    currentPassword: "",
    newPassword: "",
    confirmPassword: "",
    profileImage: null,
    primaryGoal: "presentation",
    coachingFocus: ["clarity", "pacing"],
    difficultyLevel: "intermediate",
    feedbackStyle: "detailed",
    language: "english",
    accentFocus: "neutral",
    sessionDuration: "30",
    notificationEmail: true,
    notificationSms: false,
    sessionRecording: true,
    analyticsSharing: true,
    dataPrivacy: true,
  });

  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState("");

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value,
    }));
  };

  const handleCheckboxGroup = (name, value) => {
    setFormData((prev) => ({
      ...prev,
      [name]: prev[name].includes(value)
        ? prev[name].filter((item) => item !== value)
        : [...prev[name], value],
    }));
  };

  const handleSave = (section) => {
    setMessage(`${section} settings saved successfully!`);
    setMessageType("success");
    setTimeout(() => setMessage(""), 3000);
  };

  const handleProfileImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setFormData((prev) => ({ ...prev, profileImage: reader.result }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDeleteAccount = () => {
    if (window.confirm("Are you sure you want to delete your account? This action cannot be undone.")) {
      setMessage("Account deletion initiated. Please check your email for confirmation.");
      setMessageType("warning");
    }
  };

  return (
    <div className="settings-page">
      {/* SIDEBAR */}
      <aside className="settings-sidebar">
        <div className="settings-logo">AI Speaking Coach</div>
        <nav className="settings-nav">
          {[
            { id: "profile", label: "Profile"},
            { id: "account", label: "Account Security"},
            { id: "goals", label: "Goals & Preferences"},
            { id: "coach", label: "Coach Preferences"},
            { id: "notifications", label: "Notifications"},
            { id: "privacy", label: "Privacy & Data"},
            { id: "practice", label: "Practice Settings"},
          ].map((tab) => (
            <button
              key={tab.id}
              className={`settings-nav-item ${activeTab === tab.id ? "active" : ""}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
        <button className="back-to-dashboard" onClick={() => navigate("/dashboard")}>
          ← Back to Dashboard
        </button>
      </aside>

      {/* MAIN CONTENT */}
      <main className="settings-main">
        <div className="settings-header">
          <h1>Settings</h1>
          <p>Manage your account and preferences</p>
        </div>

        {message && (
          <div className={`settings-message ${messageType}`}>
            {messageType === "success" && "✓ "}
            {messageType === "warning" && "⚠ "}
            {message}
          </div>
        )}

        {/* PROFILE TAB */}
        {activeTab === "profile" && (
          <div className="settings-section">
            <h2>Profile Information</h2>
            <div className="profile-container">
              <div className="profile-image-section">
                <div className="profile-image-wrapper">
                  {formData.profileImage ? (
                    <img src={formData.profileImage} alt="Profile" />
                  ) : (
                    <div className="profile-placeholder">JD</div>
                  )}
                </div>
                <label className="profile-upload-btn">
                  Upload Photo
                  <input
                    type="file"
                    accept="image/*"
                    hidden
                    onChange={handleProfileImageChange}
                  />
                </label>
                <p className="photo-hint">Max 5MB. JPG, PNG, or GIF.</p>
              </div>

              <div className="profile-form">
                <div className="form-group">
                  <label>Full Name</label>
                  <input
                    type="text"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleInputChange}
                    placeholder="Your full name"
                  />
                </div>

                <div className="form-group">
                  <label>Email Address</label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    placeholder="your@email.com"
                  />
                </div>

                <button
                  className="settings-save-btn primary"
                  onClick={() => handleSave("Profile")}
                >
                  Save Profile
                </button>
              </div>
            </div>
          </div>
        )}

        {/* ACCOUNT SECURITY TAB */}
        {activeTab === "account" && (
          <div className="settings-section">
            <div className="security-container">
              <div>
                <h2>Change Password</h2>
                <p className="section-description">Update your password regularly to keep your account secure.</p>
                <div className="form-group">
                  <label>Current Password</label>
                  <input
                    type="password"
                    name="currentPassword"
                    value={formData.currentPassword}
                    onChange={handleInputChange}
                    placeholder="Enter current password"
                  />
                </div>

                <div className="form-group">
                  <label>New Password</label>
                  <input
                    type="password"
                    name="newPassword"
                    value={formData.newPassword}
                    onChange={handleInputChange}
                    placeholder="Enter new password"
                  />
                  <p className="hint">At least 8 characters with uppercase, lowercase, and numbers.</p>
                </div>

                <div className="form-group">
                  <label>Confirm New Password</label>
                  <input
                    type="password"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleInputChange}
                    placeholder="Confirm new password"
                  />
                </div>

                <button
                  className="settings-save-btn primary"
                  onClick={() => handleSave("Password")}
                >
                  Update Password
                </button>
              </div>

              <div className="danger-zone">
                <h2>Danger Zone</h2>
                <p className="section-description">Irreversible and destructive actions</p>
                <button className="settings-save-btn delete" onClick={handleDeleteAccount}>
                  Delete Account
                </button>
              </div>
            </div>
          </div>
        )}

        {/* GOALS & PREFERENCES TAB */}
        {activeTab === "goals" && (
          <div className="settings-section">
            <h2>Speaking Goals & Preferences</h2>

            <div className="form-group">
              <label>Primary Speaking Goal</label>
              <select
                name="primaryGoal"
                value={formData.primaryGoal}
                onChange={handleInputChange}
              >
                <option value="presentation">Presentations & Pitches</option>
                <option value="executive">Executive Meetings</option>
                <option value="sales">Sales Pitches</option>
                <option value="conference">Conference Talks</option>
                <option value="interview">Job Interviews</option>
                <option value="general">General Public Speaking</option>
              </select>
            </div>

            <div className="form-group">
              <label>Focus Areas (Select multiple)</label>
              <div className="checkbox-group">
                {["clarity", "pacing", "confidence", "engagement", "pronunciation", "body-language"].map((area) => (
                  <label key={area} className="checkbox-item">
                    <input
                      type="checkbox"
                      checked={formData.coachingFocus.includes(area)}
                      onChange={() => handleCheckboxGroup("coachingFocus", area)}
                    />
                    <span className="checkbox-label">{area.charAt(0).toUpperCase() + area.slice(1).replace("-", " ")}</span>
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label>Difficulty Level</label>
              <select
                name="difficultyLevel"
                value={formData.difficultyLevel}
                onChange={handleInputChange}
              >
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>

            <button
              className="settings-save-btn primary"
              onClick={() => handleSave("Goals and Preferences")}
            >
              Save Preferences
            </button>
          </div>
        )}

        {/* COACH PREFERENCES TAB */}
        {activeTab === "coach" && (
          <div className="settings-section">
            <h2>AI Coach Preferences</h2>

            <div className="form-group">
              <label>Feedback Style</label>
              <select
                name="feedbackStyle"
                value={formData.feedbackStyle}
                onChange={handleInputChange}
              >
                <option value="detailed">Detailed & Comprehensive</option>
                <option value="quick">Quick Summary</option>
                <option value="balanced">Balanced</option>
              </select>
            </div>

            <div className="form-group">
              <label>Language</label>
              <select
                name="language"
                value={formData.language}
                onChange={handleInputChange}
              >
                <option value="english">English</option>
                <option value="spanish">Spanish</option>
                <option value="french">French</option>
                <option value="german">German</option>
                <option value="mandarin">Mandarin Chinese</option>
              </select>
            </div>

            <div className="form-group">
              <label>Accent & Speech Pattern Focus</label>
              <select
                name="accentFocus"
                value={formData.accentFocus}
                onChange={handleInputChange}
              >
                <option value="neutral">Neutral</option>
                <option value="american">American English</option>
                <option value="british">British English</option>
                <option value="australian">Australian English</option>
                <option value="none">No specific focus</option>
              </select>
            </div>

            <button
              className="settings-save-btn primary"
              onClick={() => handleSave("Coach Preferences")}
            >
              Save Preferences
            </button>
          </div>
        )}

        {/* NOTIFICATIONS TAB */}
        {activeTab === "notifications" && (
          <div className="settings-section">
            <h2>Notification Preferences</h2>
            <p className="section-description">Choose how you want to be notified about updates and insights.</p>

            <div className="notification-group">
              <div className="notification-item">
                <div className="notification-content">
                  <h3>Email Notifications</h3>
                  <p>Receive feedback summaries, weekly progress reports, and tips via email.</p>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    name="notificationEmail"
                    checked={formData.notificationEmail}
                    onChange={handleInputChange}
                  />
                  <span className="slider"></span>
                </label>
              </div>

              <div className="notification-item">
                <div className="notification-content">
                  <h3>SMS Notifications</h3>
                  <p>Get important alerts and reminders via text message.</p>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    name="notificationSms"
                    checked={formData.notificationSms}
                    onChange={handleInputChange}
                  />
                  <span className="slider"></span>
                </label>
              </div>
            </div>

            <button
              className="settings-save-btn primary"
              onClick={() => handleSave("Notification Settings")}
            >
              Save Notifications
            </button>
          </div>
        )}

        {/* PRIVACY & DATA TAB */}
        {activeTab === "privacy" && (
          <div className="settings-section">
            <h2>Privacy & Data Settings</h2>
            <p className="section-description">Control how your data is used and stored.</p>

            <div className="privacy-group">
              <div className="privacy-item">
                <div className="privacy-content">
                  <h3>Session Recording & Analysis</h3>
                  <p>Allow AI to analyze your recorded sessions for feedback. Your sessions are encrypted and never shared.</p>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    name="sessionRecording"
                    checked={formData.sessionRecording}
                    onChange={handleInputChange}
                  />
                  <span className="slider"></span>
                </label>
              </div>

              <div className="privacy-item">
                <div className="privacy-content">
                  <h3>Analytics & Improvement Insights</h3>
                  <p>Help us improve the AI coach by sharing anonymous analytics about your progress.</p>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    name="analyticsSharing"
                    checked={formData.analyticsSharing}
                    onChange={handleInputChange}
                  />
                  <span className="slider"></span>
                </label>
              </div>

              <div className="privacy-item">
                <div className="privacy-content">
                  <h3>Data Retention Policy</h3>
                  <p>We keep your session data for 90 days unless you choose otherwise.</p>
                </div>
                <label className="toggle-switch">
                  <input
                    type="checkbox"
                    name="dataPrivacy"
                    checked={formData.dataPrivacy}
                    onChange={handleInputChange}
                  />
                  <span className="slider"></span>
                </label>
              </div>
            </div>

            <button
              className="settings-save-btn primary"
              onClick={() => handleSave("Privacy Settings")}
            >
              Save Privacy Settings
            </button>
          </div>
        )}

        {/* PRACTICE SETTINGS TAB */}
        {activeTab === "practice" && (
          <div className="settings-section">
            <h2>Practice Settings</h2>

            <div className="form-group">
              <label>Default Session Duration</label>
              <div className="duration-options">
                {["15", "30", "45", "60"].map((duration) => (
                  <button
                    key={duration}
                    className={`duration-btn ${formData.sessionDuration === duration ? "active" : ""}`}
                    onClick={() =>
                      setFormData((prev) => ({ ...prev, sessionDuration: duration }))
                    }
                  >
                    {duration} min
                  </button>
                ))}
              </div>
            </div>

            <div className="goal-tracker">
              <h3>Practice Frequency Goals</h3>
              <p className="section-description">Set your practice schedule to build consistency.</p>
              <div className="goal-options">
                <div className="goal-card">
                  <div className="goal-icon">🎯</div>
                  <div className="goal-info">
                    <h4>Daily (Recommended)</h4>
                    <p>One session per day for optimal progress</p>
                  </div>
                </div>
                <div className="goal-card">
                  <div className="goal-icon">📅</div>
                  <div className="goal-info">
                    <h4>3x Per Week</h4>
                    <p>Build skills gradually with consistency</p>
                  </div>
                </div>
                <div className="goal-card">
                  <div className="goal-icon">💪</div>
                  <div className="goal-info">
                    <h4>Weekly</h4>
                    <p>Maintain baseline speaking confidence</p>
                  </div>
                </div>
              </div>
            </div>

            <button
              className="settings-save-btn primary"
              onClick={() => handleSave("Practice Settings")}
            >
              Save Practice Settings
            </button>
          </div>
        )}
      </main>
    </div>
  );
}
