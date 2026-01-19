import { useParams } from 'react-router-dom';
import InsightsDashboard from '../components/InsightsDashboard';

export default function InsightsPage() {
  const { draftId } = useParams<{ draftId: string }>();

  if (!draftId) {
    return (
      <div className="error">
        <h2>Invalid Draft ID</h2>
        <p>Please run a simulation first.</p>
      </div>
    );
  }

  return (
    <div className="insights-page">
      <h1>Insights & Recommendations</h1>
      <p className="page-description">
        AI-generated insights help you identify pain points and improve your content
        before publishing.
      </p>

      <InsightsDashboard draftId={parseInt(draftId)} />
    </div>
  );
}
