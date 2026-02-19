const Testimonials = () => {
  return (
    <div id="testimonials" className="testimonials">
      <div className="testimonials-container">
        <div className="section-header">
          <h2 className="section-title">What Our Users Say</h2>
          <div className="section-subtitle">
            Join thousands of professionals who have transformed their public speaking skills
          </div>
        </div>

        <div className="testimonials-grid">
          <div className="testimonial-card">
            <p className="testimonial-text">
              "This AI coach completely transformed my presentation skills. The real-time feedback
              helped me identify and fix issues I never knew I had."
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
              effective. The personalized coaching feels like having a professional trainer."
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
              how I'm improving over time."
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
  );
};

export default Testimonials;
