import type { PainPoint } from '../types/types';

interface PainPointsProps {
  painPoints: PainPoint[];
}

export default function PainPoints({ painPoints }: PainPointsProps) {
  const getSeverityClass = (severity: string) => {
    switch (severity) {
      case 'high':
        return 'severity-high';
      case 'medium':
        return 'severity-medium';
      case 'low':
        return 'severity-low';
      default:
        return '';
    }
  };

  if (!painPoints || painPoints.length === 0) {
    return (
      <div className="pain-points">
        <h3>Pain Points</h3>
        <div className="empty-state">
          <p>No significant pain points identified. Your content looks good!</p>
        </div>
      </div>
    );
  }

  // Sort by severity: high > medium > low
  const severityOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
  const sortedPainPoints = [...painPoints].sort(
    (a, b) => severityOrder[a.severity] - severityOrder[b.severity]
  );

  return (
    <div className="pain-points">
      <h3>Pain Points Identified</h3>
      <div className="pain-points-list">
        {sortedPainPoints.map((painPoint, index) => (
          <div key={index} className="pain-point-card">
            <div className="pain-point-header">
              <span className="pain-point-text">"{painPoint.text}"</span>
              <span className={`severity-badge ${getSeverityClass(painPoint.severity)}`}>
                {painPoint.severity}
              </span>
            </div>
            <div className="pain-point-details">
              <div className="affected-personas">
                <strong>Affected Personas:</strong>{' '}
                {painPoint.affected_personas.join(', ')}
              </div>
              <div className="reasoning">
                <strong>Why this matters:</strong> {painPoint.reasoning}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
