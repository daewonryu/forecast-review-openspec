import { useState } from 'react';
import type { ImprovementTip } from '../types/types';

interface ImprovementTipsProps {
  tips: ImprovementTip[];
}

export default function ImprovementTips({ tips }: ImprovementTipsProps) {
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);

  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'priority-high';
      case 'medium':
        return 'priority-medium';
      case 'low':
        return 'priority-low';
      default:
        return '';
    }
  };

  const handleCopy = async (text: string, index: number) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopiedIndex(index);
      setTimeout(() => setCopiedIndex(null), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
    }
  };

  if (!tips || tips.length === 0) {
    return (
      <div className="improvement-tips">
        <h3>Improvement Tips</h3>
        <div className="empty-state">
          <p>No improvement tips available at this time.</p>
        </div>
      </div>
    );
  }

  // Sort by priority: high > medium > low
  const priorityOrder: Record<string, number> = { high: 0, medium: 1, low: 2 };
  const sortedTips = [...tips].sort(
    (a, b) => priorityOrder[a.priority] - priorityOrder[b.priority]
  );

  return (
    <div className="improvement-tips">
      <h3>Improvement Tips</h3>
      <div className="tips-list">
        {sortedTips.map((tip, index) => (
          <div key={index} className="tip-card">
            <div className="tip-header">
              <div className="tip-category-priority">
                <span className="tip-category">{tip.category}</span>
                <span className={`priority-badge ${getPriorityClass(tip.priority)}`}>
                  {tip.priority} priority
                </span>
              </div>
              <button
                onClick={() => handleCopy(tip.suggestion, index)}
                className="copy-button"
                title="Copy suggestion"
              >
                {copiedIndex === index ? '✓' : '📋'}
              </button>
            </div>
            <div className="tip-suggestion">{tip.suggestion}</div>
            <div className="tip-impact">
              <strong>Expected Impact:</strong> {tip.expected_impact}
            </div>
            {copiedIndex === index && <div className="copy-tooltip">Copied!</div>}
          </div>
        ))}
      </div>
    </div>
  );
}
