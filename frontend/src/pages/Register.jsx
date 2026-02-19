import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/app.css";

const Register = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    fullName: "",
    email: "",
    password: "",
    confirmPassword: "",
    coachingGoal: "",
    experience: "",
    agreeTerms: false
  });

  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === "checkbox" ? checked : value
    }));
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ""
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};

    if (!formData.fullName.trim()) {
      newErrors.fullName = "Full name is required";
    }

    if (!formData.email.trim()) {
      newErrors.email = "Email is required";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = "Please enter a valid email";
    }

    if (!formData.password) {
      newErrors.password = "Password is required";
    } else if (formData.password.length < 8) {
      newErrors.password = "Password must be at least 8 characters";
    }

    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = "Passwords do not match";
    }

    if (!formData.coachingGoal) {
      newErrors.coachingGoal = "Please select a coaching goal";
    }

    if (!formData.experience) {
      newErrors.experience = "Please select your experience level";
    }

    if (!formData.agreeTerms) {
      newErrors.agreeTerms = "You must agree to the terms and conditions";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1500));

      console.log("Registration data:", formData);
      setSuccessMessage("Registration successful! Welcome to your AI Speaking Coach journey.");
      
      setTimeout(() => {
        navigate("/dashboard");
      }, 2000);
    } catch (error) {
      console.error("Registration error:", error);
      setErrors({ submit: "Registration failed. Please try again." });
    } finally {
      setIsLoading(false);
    }
  };

  const handleBackHome = () => {
    navigate("/");
  };

  return (
    <div className="register-page">
      {/* Navbar */}
      <div className="navbar navbar-register">
        <div className="nav-container">
          <button className="logo-home-btn" onClick={handleBackHome} style={{ background: "none", border: "none", cursor: "pointer", padding: 0 }}>
            <div className="logo">
              <span>AI Speaking Coach</span>
            </div>
          </button>
          <div className="nav-links">
            <button 
              className="nav-link back-link" 
              onClick={handleBackHome}
              style={{ background: "none", border: "none", cursor: "pointer", padding: "0.5rem 1rem" }}
            >
              ← Back to Home
            </button>
          </div>
        </div>
      </div>

      {/* Header Section */}
      <div className="register-hero">
        <div className="register-hero-content">
          <h1>Start Your Speaking Transformation</h1>
          <p>Join thousands of professionals mastering public speaking with AI-powered coaching</p>
        </div>
      </div>

      {/* Main Register Container */}
      <div className="register-main">
        <div className="register-layout">

          {/* Right Column - Form */}
          <div className="register-form-wrapper">
            <div className="form-card">
              <div className="form-header">
                <h2>Create Your Account</h2>
                <p>Start your journey to confident speaking</p>
              </div>

              {successMessage && (
                <div className="success-banner">
                  <div className="success-icon">✓</div>
                  <div className="success-text">{successMessage}</div>
                </div>
              )}

              <form className="register-form" onSubmit={handleSubmit}>
                {/* Full Name */}
                <div className="form-group">
                  <label htmlFor="fullName">
                    <span className="label-text">Full Name</span>
                    <span className="required">*</span>
                  </label>
                  <input
                    type="text"
                    id="fullName"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    placeholder="Enter your full name"
                    className={`form-input ${errors.fullName ? "error" : ""}`}
                  />
                  {errors.fullName && <span className="error-message">{errors.fullName}</span>}
                </div>

                {/* Email */}
                <div className="form-group">
                  <label htmlFor="email">
                    <span className="label-text">Email Address</span>
                    <span className="required">*</span>
                  </label>
                  <input
                    type="email"
                    id="email"
                    name="email"
                    value={formData.email}
                    onChange={handleChange}
                    placeholder="Enter your email address"
                    className={`form-input ${errors.email ? "error" : ""}`}
                  />
                  {errors.email && <span className="error-message">{errors.email}</span>}
                </div>

                {/* Password */}
                <div className="form-group">
                  <label htmlFor="password">
                    <span className="label-text">Password</span>
                    <span className="required">*</span>
                  </label>
                  <input
                    type="password"
                    id="password"
                    name="password"
                    value={formData.password}
                    onChange={handleChange}
                    placeholder="Enter your password at least 8 characters"
                    className={`form-input ${errors.password ? "error" : ""}`}
                  />
                  {errors.password && <span className="error-message">{errors.password}</span>}
                </div>

                {/* Confirm Password */}
                <div className="form-group">
                  <label htmlFor="confirmPassword">
                    <span className="label-text">Confirm Password</span>
                    <span className="required">*</span>
                  </label>
                  <input
                    type="password"
                    id="confirmPassword"
                    name="confirmPassword"
                    value={formData.confirmPassword}
                    onChange={handleChange}
                    placeholder="Confirm your password"
                    className={`form-input ${errors.confirmPassword ? "error" : ""}`}
                  />
                  {errors.confirmPassword && <span className="error-message">{errors.confirmPassword}</span>}
                </div>


                {/* Terms Agreement */}
                <div className="form-group checkbox-group">
                  <div className="checkbox-wrapper">
                    <input
                      type="checkbox"
                      id="agreeTerms"
                      name="agreeTerms"
                      checked={formData.agreeTerms}
                      onChange={handleChange}
                      className={`checkbox-input ${errors.agreeTerms ? "error" : ""}`}
                    />
                    <label htmlFor="agreeTerms" className="checkbox-label">
                      I agree to the <a href="#terms" className="link">Terms and Conditions</a> and <a href="#privacy" className="link">Privacy Policy</a>
                      <span className="required">*</span>
                    </label>
                  </div>
                  {errors.agreeTerms && <span className="error-message">{errors.agreeTerms}</span>}
                </div>

                {errors.submit && (
                  <div className="error-banner">
                    <div className="error-icon">⚠</div>
                    <div className="error-text">{errors.submit}</div>
                  </div>
                )}

                {/* Submit Button */}
                <button
                  type="submit"
                  className="submit-button"
                  disabled={isLoading || successMessage}
                >
                  {isLoading ? (
                    <>
                      <span className="spinner"></span>
                      Creating Your Account...
                    </>
                  ) : successMessage ? (
                    <>
                      <span className="checkmark">✓</span>
                      Registration Successful
                    </>
                  ) : (
                    "Create My Account"
                  )}
                </button>

                {/* Login Link */}
                <div className="form-footer">
                  <p>Already have an account? <button 
                    onClick={() => navigate("/")}
                    style={{ background: "none", border: "none", color: "#4f46e5", cursor: "pointer", textDecoration: "underline", fontWeight: "600" }}
                  >
                    Sign in here
                  </button></p>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>

      {/* Security Info Footer */}
      
    </div>
  );
};

export default Register;
