import type { SimulationResponse } from '../types/types';
import PersonaReaction from './PersonaReaction';

interface SimulationResultsProps {
  results: SimulationResponse;
  onGenerateInsights?: () => void;
}

export default function SimulationResults({
  results,
  onGenerateInsights,
}: SimulationResultsProps) {
  const getScoreClass = (score: number, isBacklash: boolean = false) => {
    if (isBacklash) {
      // Backlash: high score is bad
      if (score >= 8) return 'score-bad';
      if (score >= 5) return 'score-warning';
      return 'score-good';
    } else {
      // Trust/Excitement: high score is good
      if (score >= 8) return 'score-good';
      if (score >= 5) return 'score-warning';
      return 'score-bad';
    }
  };

  return (
    <div className="simulation-results">
      <div className="results-header">
        <h2>Simulation Results</h2>
        <div className="results-meta">
          <span>Completed in {results.duration_seconds.toFixed(1)}s</span>
          <span className="separator">•</span>
          <span>{new Date(results.completed_at).toLocaleString()}</span>
        </div>
      </div>

      <div className="aggregate-scores">
        <h3>Overall Scores</h3>
        <div className="scores-grid">
          <div className={`score-card ${getScoreClass(results.aggregate.avg_trust)}`}>
            <div className="score-label">Average Trust</div>
            <div className="score-value">{results.aggregate.avg_trust.toFixed(1)}</div>
            <div className="score-max">/ 10</div>
          </div>
          <div className={`score-card ${getScoreClass(results.aggregate.avg_excitement)}`}>
            <div className="score-label">Average Excitement</div>
            <div className="score-value">
              {results.aggregate.avg_excitement.toFixed(1)}
            </div>
            <div className="score-max">/ 10</div>
          </div>
          <div
            className={`score-card ${getScoreClass(results.aggregate.avg_backlash_risk, true)}`}
          >
            <div className="score-label">Average Backlash Risk</div>
            <div className="score-value">{results.aggregate.avg_backlash_risk.toFixed(1)}</div>
            <div className="score-max">/ 10</div>
          </div>
        </div>
      </div>

      <div className="persona-reactions">
        <h3>Individual Persona Reactions</h3>
        <div className="reactions-grid">
          {results.results.map((result: any) => (
            <PersonaReaction key={result.persona_id} result={result} />
          ))}
        </div>
      </div>

      {onGenerateInsights && (
        <div className="actions">
          <button onClick={onGenerateInsights} className="btn-primary btn-large">
            View Insights & Improvement Tips
          </button>
        </div>
      )}
    </div>
  );
}
