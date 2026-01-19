import type { SimulationResult } from '../types/types';

interface PersonaReactionProps {
  result: SimulationResult;
}

export default function PersonaReaction({ result }: PersonaReactionProps) {
  const getScoreBadgeClass = (score: number, isBacklash: boolean = false) => {
    if (isBacklash) {
      if (score >= 8) return 'badge-danger';
      if (score >= 5) return 'badge-warning';
      return 'badge-success';
    } else {
      if (score >= 8) return 'badge-success';
      if (score >= 5) return 'badge-warning';
      return 'badge-danger';
    }
  };

  if (result.status !== 'success') {
    return (
      <div className="persona-reaction error">
        <h4>{result.persona_name}</h4>
        <p className="error-text">
          This persona simulation failed. Overall results are based on successful personas
          only.
        </p>
      </div>
    );
  }

  return (
    <div className="persona-reaction">
      <div className="reaction-header">
        <h4>{result.persona_name}</h4>
        <div className="scores-row">
          <span className={`score-badge ${getScoreBadgeClass(result.scores.trust)}`}>
            Trust: {result.scores.trust}/10
          </span>
          <span className={`score-badge ${getScoreBadgeClass(result.scores.excitement)}`}>
            Excitement: {result.scores.excitement}/10
          </span>
          <span
            className={`score-badge ${getScoreBadgeClass(result.scores.backlash_risk, true)}`}
          >
            Backlash: {result.scores.backlash_risk}/10
          </span>
        </div>
      </div>

      <div className="reaction-content">
        <div className="reaction-section">
          <h5>Internal Reaction</h5>
          <p className="internal-reaction">{result.internal_monologue}</p>
        </div>

        <div className="reaction-section">
          <h5>Public Response</h5>
          <p className="public-response">{result.public_comment}</p>
        </div>

        {result.reasoning && (
          <div className="reaction-section">
            <h5>Reasoning</h5>
            <p className="reasoning">{result.reasoning}</p>
          </div>
        )}
      </div>
    </div>
  );
}
