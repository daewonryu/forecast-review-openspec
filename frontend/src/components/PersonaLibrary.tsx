import { useQuery } from '@tanstack/react-query';
import { listPersonaSets } from '../api';
import type { PersonaSetSummary } from '../types/types';

interface PersonaLibraryProps {
  userId: number;
  onSelectSet?: (setId: string) => void;
  selectedSetId?: string;
}

export default function PersonaLibrary({
  userId,
  onSelectSet,
  selectedSetId,
}: PersonaLibraryProps) {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ['personaSets', userId],
    queryFn: () => listPersonaSets(userId, 1, 50),
  });

  if (isLoading) return <div className="loading">Loading persona sets...</div>;
  if (error) return <div className="error">Error loading persona sets</div>;

  return (
    <div className="persona-library">
      <div className="library-header">
        <h2>Your Persona Sets</h2>
        <button onClick={() => refetch()} className="btn-secondary">
          Refresh
        </button>
      </div>

      {data && data.sets.length === 0 ? (
        <div className="empty-state">
          <p>No persona sets yet. Generate your first set above!</p>
        </div>
      ) : (
        <div className="persona-sets-grid">
          {data?.sets.map((set: PersonaSetSummary) => (
            <div
              key={set.set_id}
              className={`persona-set-card ${
                selectedSetId === set.set_id ? 'selected' : ''
              }`}
              onClick={() => onSelectSet?.(set.set_id)}
            >
              <h3>{set.audience_description}</h3>
              <div className="set-meta">
                <span className="persona-count">
                  {set.persona_count} personas
                </span>
                <span className="created-date">
                  {new Date(set.created_at).toLocaleDateString()}
                </span>
              </div>
              {selectedSetId === set.set_id && (
                <div className="selected-badge">✓ Selected</div>
              )}
            </div>
          ))}
        </div>
      )}

      {data && (
        <div className="pagination-info">
          Showing {data.sets.length} of {data.total} sets
        </div>
      )}
    </div>
  );
}
