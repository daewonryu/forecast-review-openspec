import type { Persona } from '../types/types';

interface PersonaCardProps {
  persona: Persona;
  compact?: boolean;
}

export default function PersonaCard({ persona, compact = false }: PersonaCardProps) {
  return (
    <div className={`persona-card ${compact ? 'compact' : ''}`}>
      <h4 className="persona-name">{persona.name}</h4>
      <p className="persona-archetype">{persona.archetype}</p>
      <div className="loyalty-level">
        <span className="label">Loyalty:</span>
        <div className="loyalty-bar">
          <div
            className="loyalty-fill"
            style={{ width: `${(persona.loyalty_level / 10) * 100}%` }}
          ></div>
        </div>
        <span className="loyalty-score">{persona.loyalty_level}/10</span>
      </div>
      <div className="core-values">
        {persona.core_values.map((value: string, index: number) => (
          <span key={index} className="value-tag">
            {value}
          </span>
        ))}
      </div>
    </div>
  );
}
