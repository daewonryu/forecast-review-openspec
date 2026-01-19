import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { listSimulations } from '../api';
import LoadingSpinner from '../components/LoadingSpinner';

const USER_ID = 1; // MVP: Hard-coded user ID

export default function HistoryPage() {
  const navigate = useNavigate();
  
  const { data, isLoading, error } = useQuery({
    queryKey: ['simulations', USER_ID],
    queryFn: () => listSimulations(USER_ID, 1, 50),
  });

  if (isLoading) return <LoadingSpinner />;
  if (error) return <div className="error">Error loading simulation history</div>;

  return (
    <div className="history-page">
      <h1>Simulation History</h1>
      <p className="page-description">
        View your past simulations and their results.
      </p>

      {data && data.simulations && data.simulations.length === 0 ? (
        <div className="empty-state">
          <p>No simulations yet. Run your first simulation to see results here!</p>
        </div>
      ) : (
        <div className="simulations-list">
          {data?.simulations?.map((simulation: any) => (
            <div 
              key={simulation.simulation_id} 
              className="simulation-card clickable"
              onClick={() => navigate(`/insights/${simulation.draft_id}`)}
              style={{ cursor: 'pointer' }}
            >
              <div className="simulation-header">
                <span className="simulation-date">
                  {new Date(simulation.completed_at).toLocaleString()}
                </span>
                <span className="simulation-duration">
                  {simulation.duration_seconds}s
                </span>
              </div>
              <p className="draft-preview">
                {simulation.draft_content?.substring(0, 150)}
                {simulation.draft_content?.length > 150 ? '...' : ''}
              </p>
              <div className="simulation-scores">
                <span className="score">
                  Trust: {simulation.aggregate?.avg_trust?.toFixed(1)}/10
                </span>
                <span className="score">
                  Excitement: {simulation.aggregate?.avg_excitement?.toFixed(1)}/10
                </span>
                <span className="score">
                  Backlash: {simulation.aggregate?.avg_backlash?.toFixed(1)}/10
                </span>
              </div>
              <div className="view-details-hint">
                Click to view full details →
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
