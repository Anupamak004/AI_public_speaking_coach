import { Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/dashboard";
import SpeakerProgress from "./pages/SpeakerProgress";
import SessionHistory from "./pages/SessionHistory";
import Settings from "./pages/Settings";
import Register from "./pages/Register";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/speaker-progress" element={<SpeakerProgress />} />
      <Route path="/session-history" element={<SessionHistory />} />
      <Route path="/settings" element={<Settings />} />
    </Routes>
  );
}

export default App;
