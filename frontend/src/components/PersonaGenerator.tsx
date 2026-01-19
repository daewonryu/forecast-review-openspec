import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { generatePersonas } from '../api';
import type { PersonaGenerateRequest } from '../types/types';

interface PersonaGeneratorProps {
  userId: number;
  onPersonasGenerated?: (setId: string) => void;
}

export default function PersonaGenerator({ userId, onPersonasGenerated }: PersonaGeneratorProps) {
  const [audienceDescription, setAudienceDescription] = useState('');

  const mutation = useMutation({
    mutationFn: (request: PersonaGenerateRequest) =>
      generatePersonas(request),
    onSuccess: (data: any) => {
      setAudienceDescription('');
      if (onPersonasGenerated) {
        onPersonasGenerated(data.set_id);
      }
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (audienceDescription.trim().length < 5) {
      alert('Audience description must be at least 5 characters');
      return;
    }
    mutation.mutate({
      audience_description: audienceDescription,
      save_to_library: true,
    });
  };

  return (
    <div className="persona-generator">
      <h2>Generate Personas</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="audience">
            Describe Your Audience
            <span className="help-text">
              (e.g., "Tech enthusiasts interested in AI and machine learning")
            </span>
          </label>
          <textarea
            id="audience"
            value={audienceDescription}
            onChange={(e) => setAudienceDescription(e.target.value)}
            placeholder="Describe your target audience..."
            rows={4}
            minLength={5}
            maxLength={500}
            required
            disabled={mutation.isPending}
          />
          <div className="char-count">
            {audienceDescription.length} / 500
          </div>
        </div>

        <button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? 'Generating...' : 'Generate 5 Personas'}
        </button>
      </form>

      {mutation.isError && (
        <div className="error">
          Error generating personas: {mutation.error.message}
        </div>
      )}

      {mutation.isSuccess && mutation.data && (
        <div className="success">
          <h3>✓ Personas Generated Successfully!</h3>
          <div className="personas-preview">
            {mutation.data.personas.map((persona: any) => (
              <div key={persona.id} className="persona-card">
                <h4>{persona.name}</h4>
                <p className="archetype">{persona.archetype}</p>
                <div className="loyalty">
                  Loyalty: {persona.loyalty_level}/10
                </div>
                <div className="values">
                  Values: {persona.core_values.join(', ')}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
