import { Link, Outlet, useLocation } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { checkHealth } from '../api';

export default function Layout() {
  const location = useLocation();
  const { data: health } = useQuery({
    queryKey: ['health'],
    queryFn: checkHealth,
    refetchInterval: 30000, // Check every 30 seconds
  });

  const isActive = (path: string) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  return (
    <div className="layout">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <Link to="/" className="logo">
              <h1>FanEcho</h1>
            </Link>
            <nav className="nav">
              <Link
                to="/"
                className={isActive('/') && location.pathname === '/' ? 'active' : ''}
              >
                Home
              </Link>
              <Link to="/personas" className={isActive('/personas') ? 'active' : ''}>
                Personas
              </Link>
              <Link to="/simulate" className={isActive('/simulate') ? 'active' : ''}>
                Simulate
              </Link>
              <Link to="/history" className={isActive('/history') ? 'active' : ''}>
                History
              </Link>
            </nav>
            <div className="health-status">
              {health ? (
                <span className="status-healthy" title="API Connected">
                  ●
                </span>
              ) : (
                <span className="status-error" title="API Disconnected">
                  ●
                </span>
              )}
            </div>
          </div>
        </div>
      </header>
      <main className="main">
        <div className="container">
          <Outlet />
        </div>
      </main>
      <footer className="footer">
        <div className="container">
          <p>&copy; 2026 FanEcho. AI-powered fan reaction simulator.</p>
        </div>
      </footer>
    </div>
  );
}
