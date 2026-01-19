import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import SimulationForm from '../components/SimulationForm';
import SimulationResults from '../components/SimulationResults';
import type { SimulationResponse } from '../types/types';

const USER_ID = 1; // MVP: Hard-coded user ID

export default function SimulatePage() {
  const [simulationResults, setSimulationResults] = useState<SimulationResponse | null>(
    null
  );
  const navigate = useNavigate();

  const handleSimulationComplete = (results: SimulationResponse) => {
    setSimulationResults(results);
  };

  const handleGenerateInsights = () => {
    if (simulationResults) {
      navigate(`/insights/${simulationResults.draft_id}`);
    }
  };

  return (
    <div className="simulate-page">
      <h1>Run Simulation</h1>
      <p className="page-description">
        Enter your draft content and select a persona set to see how your audience will
        react. Simulations typically complete in 10-20 seconds.
      </p>

      <SimulationForm userId={USER_ID} onSimulationComplete={handleSimulationComplete} />

      {simulationResults && (
        <SimulationResults
          results={simulationResults}
          onGenerateInsights={handleGenerateInsights}
        />
      )}
    </div>
  );
}
