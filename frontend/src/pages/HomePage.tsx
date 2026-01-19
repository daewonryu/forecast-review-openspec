import { Link } from 'react-router-dom';

export default function HomePage() {
  return (
    <div className="home-page">
      <section className="hero">
        <h1>Welcome to FanEcho</h1>
        <p className="subtitle">
          Test your content with AI-powered synthetic fan personas before you post
        </p>
        <p className="description">
          FanEcho helps you avoid PR disasters by simulating how your audience will react
          to announcements, social media posts, and marketing content. Get insights on
          trust, excitement, and backlash risk in under 20 seconds.
        </p>
      </section>

      <section className="getting-started">
        <h2>Get Started in 3 Steps</h2>
        <div className="steps">
          <div className="step">
            <div className="step-number">1</div>
            <h3>Generate Personas</h3>
            <p>Describe your audience and we'll create 5 diverse AI personas</p>
            <Link to="/personas" className="btn-primary">
              Create Personas
            </Link>
          </div>
          <div className="step">
            <div className="step-number">2</div>
            <h3>Run Simulation</h3>
            <p>Enter your draft content and see how each persona reacts</p>
            <Link to="/simulate" className="btn-primary">
              Start Simulation
            </Link>
          </div>
          <div className="step">
            <div className="step-number">3</div>
            <h3>Show History</h3>
            <p>Get actionable improvement tips and identify pain points</p>
            <Link to="/history" className="btn-primary">
              Show History
            </Link>
          </div>
        </div>
      </section>

      <section className="features">
        <h2>Why FanEcho?</h2>
        <div className="feature-grid">
          <div className="feature">
            <h3>⚡ Fast</h3>
            <p>Get complete simulation results in 10-20 seconds</p>
          </div>
          <div className="feature">
            <h3>🎯 Accurate</h3>
            <p>AI personas capture diverse perspectives and loyalty levels</p>
          </div>
          <div className="feature">
            <h3>💡 Actionable</h3>
            <p>Receive specific improvement tips to optimize your content</p>
          </div>
          <div className="feature">
            <h3>🔒 Private</h3>
            <p>Your drafts stay confidential - test before you publish</p>
          </div>
        </div>
      </section>
    </div>
  );
}
