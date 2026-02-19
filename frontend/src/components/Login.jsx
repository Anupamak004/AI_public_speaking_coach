import { useState } from "react";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!email || !password) {
      alert("Please enter email and password");
      return;
    }

    alert("Login successful!");
  };

  return (
    <div id="login-section" className="login-container">
      <form className="stForm" onSubmit={handleSubmit}>
        <h1 style={{ textAlign: "center", color: "black" }}>
          Login to Your Account
        </h1>
        <p style={{ textAlign: "center", color: "#6b7280" }}>
          Continue your speaking journey
        </p>

        <label>Email Address</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />

        <label>Password</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
