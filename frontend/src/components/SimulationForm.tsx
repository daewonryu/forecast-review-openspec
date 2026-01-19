import { useState, useEffect } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { runSimulation, listPersonaSets } from '../api';
import type { SimulationRequest, SimulationResponse } from '../types/types';
import LoadingSpinner from './LoadingSpinner';

interface SimulationFormProps {
  userId: number;
  onSimulationComplete?: (results: SimulationResponse) => void;
}

export default function SimulationForm({
  userId,
  onSimulationComplete,
}: SimulationFormProps) {
  const [draftContent, setDraftContent] = useState('');
  const [selectedSetId, setSelectedSetId] = useState<string>('');

  const { data: personaSetsData, isLoading: loadingSets } = useQuery({
    queryKey: ['personaSets', userId],
    queryFn: () => listPersonaSets(userId, 1, 50),
  });

  useEffect(() => {
    if (personaSetsData?.sets && personaSetsData.sets.length > 0 && !selectedSetId) {
      setSelectedSetId(personaSetsData.sets[0].set_id);
    }
  }, [personaSetsData, selectedSetId]);

  const mutation = useMutation({
    mutationFn: (request: SimulationRequest) => runSimulation(request),
    onSuccess: (data) => {
      if (onSimulationComplete) {
        onSimulationComplete(data);
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (draftContent.trim().length < 10) {
      alert('Draft content must be at least 10 characters');
      return;
    }

    if (!selectedSetId) {
      alert('Please select a persona set');
      return;
    }

    mutation.mutate({
      draft_content: draftContent,
      persona_set_id: selectedSetId,
    });
  };

  if (loadingSets) return <LoadingSpinner />;

  if (!personaSetsData?.sets || personaSetsData.sets.length === 0) {
    return (
      <div className="empty-state">
        <h3>No Persona Sets Found</h3>
        <p>Please generate personas first before running a simulation.</p>
        <a href="/personas" className="btn-primary">
          Go to Personas
        </a>
      </div>
    );
  }

  return (
    <div className="simulation-form">
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="personaSet">
            Select Persona Set
            <span className="required">*</span>
          </label>
          <select
            id="personaSet"
            value={selectedSetId}
            onChange={(e) => setSelectedSetId(e.target.value)}
            disabled={mutation.isPending}
            required
          >
            <option value="">-- Select a persona set --</option>
            {personaSetsData.sets.map((set: any) => (
              <option key={set.set_id} value={set.set_id}>
                {set.audience_description} ({set.persona_count} personas)
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="draftContent">
            Draft Content
            <span className="required">*</span>
            <span className="help-text">
              Enter the content you want to test (e.g., social media post, announcement)
            </span>
          </label>
          <textarea
            id="draftContent"
            value={draftContent}
            onChange={(e) => setDraftContent(e.target.value)}
            placeholder="Enter your draft content here..."
            rows={8}
            minLength={10}
            maxLength={5000}
            required
            disabled={mutation.isPending}
          />
          <div className="char-count">
            {draftContent.length} / 5000 characters
            {draftContent.length < 10 && (
              <span className="error-text"> (minimum 10)</span>
            )}
          </div>
        </div>

        <button
          type="submit"
          className="btn-primary btn-large"
          disabled={mutation.isPending || !selectedSetId}
        >
          {mutation.isPending ? 'Running Simulation...' : 'Run Simulation'}
        </button>

        {mutation.isPending && (
          <div className="simulation-progress">
            <LoadingSpinner />
            <p>Analyzing your draft with 5 personas...</p>
            <p className="help-text">This typically takes 10-20 seconds</p>
          </div>
        )}

        {mutation.isError && (
          <div className="error-message">
            <strong>Error:</strong> {mutation.error?.message || 'Failed to run simulation'}
          </div>
        )}
      </form>
    </div>
  );
}
