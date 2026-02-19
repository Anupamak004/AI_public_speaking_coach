const Navbar = () => {
  return (
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
  );
};

export default Navbar;
