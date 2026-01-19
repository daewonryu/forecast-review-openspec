import { useMutation, useQuery } from '@tanstack/react-query';
import { generateInsights, getInsights } from '../api';
import LoadingSpinner from './LoadingSpinner';
import PainPoints from './PainPoints';
import ImprovementTips from './ImprovementTips';

interface InsightsDashboardProps {
  draftId: number;
}

export default function InsightsDashboard({ draftId }: InsightsDashboardProps) {
  const { data: existingInsights, isLoading } = useQuery({
    queryKey: ['insights', draftId],
    queryFn: () => getInsights(draftId),
    retry: false,
  });

  const mutation = useMutation({
    mutationFn: () => generateInsights(draftId),
  });

  const insights = mutation.data || existingInsights;

  if (isLoading) return <LoadingSpinner />;

  if (!insights && !mutation.isPending) {
    return (
      <div className="insights-empty">
        <h3>Generate Insights</h3>
        <p>Click the button below to generate AI-powered insights for this draft.</p>
        <button
          onClick={() => mutation.mutate()}
          className="btn-primary btn-large"
          disabled={mutation.isPending}
        >
          Generate Insights
        </button>
        {mutation.isError && (
          <div className="error-message">
            Failed to generate insights. Please try again.
          </div>
        )}
      </div>
    );
  }

  if (mutation.isPending) {
    return (
      <div className="insights-loading">
        <LoadingSpinner />
        <p>Generating insights...</p>
        <p className="help-text">This typically takes 5-10 seconds</p>
      </div>
    );
  }

  if (!insights) return null;

  return (
    <div className="insights-dashboard">
      <div className="insights-summary">
        <h3>Overall Sentiment</h3>
        <div className={`sentiment-badge-large sentiment-${insights.overall_sentiment}`}>
          {insights.overall_sentiment}
        </div>
      </div>

      <div className="aggregate-analytics">
        <h3>Aggregate Analytics</h3>
        <div className="analytics-grid">
          <div className="analytic-card">
            <div className="analytic-label">Average Trust</div>
            <div className="analytic-value">
              {insights.avg_trust.toFixed(1)}
            </div>
            <div className="analytic-max">/ 10</div>
          </div>
          <div className="analytic-card">
            <div className="analytic-label">Average Excitement</div>
            <div className="analytic-value">
              {insights.avg_excitement.toFixed(1)}
            </div>
            <div className="analytic-max">/ 10</div>
          </div>
          <div className="analytic-card">
            <div className="analytic-label">Average Backlash Risk</div>
            <div className="analytic-value">
              {insights.avg_backlash_risk.toFixed(1)}
            </div>
            <div className="analytic-max">/ 10</div>
          </div>
        </div>
      </div>

      <PainPoints painPoints={insights.pain_points} />

      <ImprovementTips tips={insights.improvement_tips} />
    </div>
  );
}
