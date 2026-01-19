import { useState } from 'react';
import PersonaGenerator from '../components/PersonaGenerator';
import PersonaLibrary from '../components/PersonaLibrary';

const USER_ID = 1; // MVP: Hard-coded user ID

export default function PersonasPage() {
  const [selectedSetId, setSelectedSetId] = useState<string | undefined>();
  const [refreshKey, setRefreshKey] = useState(0);

  const handlePersonasGenerated = (setId: string) => {
    setSelectedSetId(setId);
    setRefreshKey((prev) => prev + 1); // Trigger library refresh
  };

  return (
    <div className="personas-page">
      <h1>Persona Management</h1>
      <p className="page-description">
        Generate diverse AI personas that represent your audience, then reuse them across
        multiple content simulations.
      </p>

      <PersonaGenerator userId={USER_ID} onPersonasGenerated={handlePersonasGenerated} />

      <PersonaLibrary
        key={refreshKey}
        userId={USER_ID}
        onSelectSet={setSelectedSetId}
        selectedSetId={selectedSetId}
      />
    </div>
  );
}
