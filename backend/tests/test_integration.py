"""
Integration tests for FanEcho MVP end-to-end workflows
"""
import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from unittest.mock import patch, AsyncMock
import json

from app.main import app
from app.db.database import Base, get_db
from app.db.models import User, Persona, Draft, SimulationResult, Insight

# Test database setup
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def test_db():
    """Create test database"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(test_db):
    """Create test client with database override"""
    def override_get_db():
        try:
            yield test_db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(test_db):
    """Create test user"""
    from app.db.models import User
    user = User(email="test@example.com", username="testuser")
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


class TestPersonaWorkflow:
    """End-to-end tests for persona generation workflow"""
    
    @pytest.mark.asyncio
    async def test_full_persona_generation_flow(self, client, test_user):
        """Test complete persona generation and retrieval flow"""
        
        # Mock LLM responses
        with patch('app.services.llm.LLMService.generate') as mock_generate:
            mock_generate.return_value = {
                "content": json.dumps({
                    "personas": [
                        {
                            "name": f"Persona {i}",
                            "archetype": f"Archetype {i}",
                            "loyalty_level": i + 3,
                            "core_values": ["Value1", "Value2"]
                        }
                        for i in range(5)
                    ]
                }),
                "cost": 0.01,
                "duration": 1.5
            }
            
            # Step 1: Generate personas
            response = client.post(
                "/api/personas/generate",
                json={
                    "audience_description": "Tech enthusiasts interested in AI",
                    "user_id": test_user.id
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "set_id" in data
            assert len(data["personas"]) == 5
            set_id = data["set_id"]
            
            # Step 2: Retrieve persona set
            response = client.get(f"/api/personas/sets/{set_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["set_id"] == set_id
            assert len(data["personas"]) == 5
            
            # Step 3: List all persona sets for user
            response = client.get(f"/api/personas/sets?user_id={test_user.id}")
            assert response.status_code == 200
            data = response.json()
            assert len(data) >= 1


class TestSimulationWorkflow:
    """End-to-end tests for simulation workflow"""
    
    @pytest.mark.asyncio
    async def test_full_simulation_flow(self, client, test_user, test_db):
        """Test complete simulation flow from draft submission to results"""
        
        # Setup: Create personas
        personas = []
        set_id = "test-set-123"
        for i in range(5):
            persona = Persona(
                set_id=set_id,
                name=f"Persona {i}",
                archetype=f"Archetype {i}",
                loyalty_level=i + 3,
                core_values=["Value1", "Value2"],
                audience_description="Test audience",
                user_id=test_user.id
            )
            test_db.add(persona)
            personas.append(persona)
        test_db.commit()
        
        # Mock LLM responses for reactions
        with patch('app.services.llm.LLMService.generate') as mock_generate:
            mock_generate.return_value = {
                "content": json.dumps({
                    "internal_reaction": "This is interesting",
                    "public_response": "Looks good!",
                    "trust_score": 7,
                    "excitement_score": 8,
                    "backlash_score": 2,
                    "reasoning": "The content is well-written"
                }),
                "cost": 0.01,
                "duration": 1.0
            }
            
            # Step 1: Run simulation
            response = client.post(
                "/api/simulations/run",
                json={
                    "draft_content": "Exciting new AI product launching soon!",
                    "persona_set_id": set_id,
                    "user_id": test_user.id
                }
            )
            
            assert response.status_code == 200
            data = response.json()
            assert "simulation_id" in data
            assert "results" in data
            assert len(data["results"]) == 5
            assert "aggregate" in data
            
            simulation_id = data["simulation_id"]
            draft_id = data["draft_id"]
            
            # Step 2: Retrieve simulation results
            response = client.get(f"/api/simulations/{simulation_id}")
            assert response.status_code == 200
            data = response.json()
            assert data["simulation_id"] == simulation_id
            
            # Step 3: Generate insights
            response = client.post(f"/api/insights/generate/{draft_id}")
            assert response.status_code == 200
            data = response.json()
            assert "aggregate_analytics" in data
            assert "pain_points" in data
            assert "improvement_tips" in data
            
            # Step 4: Retrieve insights
            insight_id = data["id"]
            response = client.get(f"/api/insights/{insight_id}")
            assert response.status_code == 200


class TestInsightsWorkflow:
    """End-to-end tests for insights generation"""
    
    @pytest.mark.asyncio
    async def test_insights_generation_flow(self, client, test_user, test_db):
        """Test insights generation from simulation results"""
        
        # Setup: Create draft and simulation results
        draft = Draft(
            content="Test draft content",
            user_id=test_user.id
        )
        test_db.add(draft)
        test_db.commit()
        test_db.refresh(draft)
        
        # Create personas and results
        for i in range(5):
            persona = Persona(
                set_id="test-set",
                name=f"Persona {i}",
                archetype=f"Archetype {i}",
                loyalty_level=i + 3,
                core_values=["Value1", "Value2"],
                audience_description="Test audience",
                user_id=test_user.id
            )
            test_db.add(persona)
            test_db.commit()
            test_db.refresh(persona)
            
            result = SimulationResult(
                simulation_id="test-sim-123",
                draft_id=draft.id,
                persona_id=persona.id,
                internal_monologue="Internal thought",
                public_comment="Public comment",
                trust_score=6,
                excitement_score=7,
                backlash_risk_score=3,
                reasoning="Test reasoning",
                status="success"
            )
            test_db.add(result)
        
        test_db.commit()
        
        # Mock LLM responses
        with patch('app.services.llm.LLMService.generate') as mock_generate:
            # Mock pain points extraction
            mock_generate.side_effect = [
                json.dumps([{
                    "text": "problematic phrase",
                    "severity": "high",
                    "affected_personas": ["Persona 0", "Persona 1"],
                    "reasoning": "Comes across as insensitive"
                }]),
                json.dumps([{
                    "tip": "Replace 'X' with 'Y'",
                    "rationale": "More appropriate tone",
                    "impact": "high",
                    "addresses": ["problematic phrase"]
                }] * 3)
            ]
            
            # Generate insights
            response = client.post(f"/api/insights/generate/{draft.id}")
            assert response.status_code == 200
            data = response.json()
            
            assert data["draft_id"] == draft.id
            assert len(data["pain_points"]) > 0
            assert len(data["improvement_tips"]) > 0


class TestPersonaDrillDown:
    """Tests for persona drill-down functionality"""
    
    def test_persona_comparison(self, client, test_user, test_db):
        """Test persona drill-down view"""
        
        # Setup: Create draft and results
        draft = Draft(
            content="Test draft",
            user_id=test_user.id,
            persona_set_id="test-set"
        )
        test_db.add(draft)
        test_db.commit()
        test_db.refresh(draft)
        
        # Create personas with varying scores
        for i in range(5):
            persona = Persona(
                set_id="test-set",
                name=f"Persona {i}",
                archetype=f"Archetype {i}",
                loyalty_level=i + 3,
                core_values=["Value1", "Value2"],
                audience_description="Test audience",
                user_id=test_user.id
            )
            test_db.add(persona)
            test_db.commit()
            test_db.refresh(persona)
            
            # Persona 4 will be an outlier
            trust_score = 9 if i == 4 else 5
            
            result = SimulationResult(
                simulation_id="test-sim-123",
                draft_id=draft.id,
                persona_id=persona.id,
                internal_monologue="Internal",
                public_comment="Public",
                trust_score=trust_score,
                excitement_score=5,
                backlash_risk_score=3,
                reasoning="Reasoning",
                status="success"
            )
            test_db.add(result)
        
        test_db.commit()
        
        # Get drill-down for outlier
        personas_list = test_db.query(Persona).filter(Persona.name == "Persona 4").all()
        if personas_list:
            persona_id = personas_list[0].id
            
            response = client.get(
                f"/api/insights/persona/{persona_id}/drill-down?draft_id={draft.id}"
            )
            
            assert response.status_code == 200
            data = response.json()
            assert data["is_outlier"] == True
            assert data["delta"]["trust"] > 0  # Above average


class TestSentimentTrends:
    """Tests for sentiment tracking over time"""
    
    def test_trend_tracking(self, client, test_user, test_db):
        """Test sentiment trends across multiple simulations"""
        
        # Create personas
        set_id = "trend-test"
        personas = []
        for i in range(5):
            persona = Persona(
                set_id=set_id,
                name=f"Persona {i}",
                archetype=f"Archetype {i}",
                loyalty_level=5,
                core_values=["Value1", "Value2"],
                audience_description="Test",
                user_id=test_user.id
            )
            test_db.add(persona)
            test_db.commit()
            test_db.refresh(persona)
            personas.append(persona)
        
        # Create multiple drafts and simulations
        for draft_num in range(3):
            draft = Draft(
                content=f"Draft {draft_num} content",
                user_id=test_user.id
            )
            test_db.add(draft)
            test_db.commit()
            test_db.refresh(draft)
            
            # Improving scores over time
            base_score = 5 + draft_num
            for persona in personas:
                result = SimulationResult(
                    simulation_id=f"sim-{draft_num}",
                    draft_id=draft.id,
                    persona_id=persona.id,
                    internal_monologue="Test",
                    public_comment="Test",
                    trust_score=base_score,
                    excitement_score=base_score,
                    backlash_risk_score=7 - draft_num,  # Decreasing
                    reasoning="Test",
                    status="success"
                )
                test_db.add(result)
        
        test_db.commit()
        
        # Get trends
        response = client.get(f"/api/insights/trends/{set_id}?user_id={test_user.id}")
        assert response.status_code == 200
        data = response.json()
        
        assert len(data["simulations"]) == 3
        # Check improvement
        if len(data["simulations"]) > 1:
            second_sim = data["simulations"][1]
            assert second_sim["delta_from_previous"] is not None
            assert second_sim["delta_from_previous"]["trust"] > 0


class TestErrorHandling:
    """Tests for error handling and edge cases"""
    
    def test_simulation_with_missing_personas(self, client, test_user):
        """Test simulation with non-existent persona set"""
        response = client.post(
            "/api/simulations/run",
            json={
                "draft_content": "Test content",
                "persona_set_id": "non-existent",
                "user_id": test_user.id
            }
        )
        
        assert response.status_code in [404, 400, 500]
    
    def test_insights_for_non_existent_draft(self, client):
        """Test insights generation for missing draft"""
        response = client.post("/api/insights/generate/99999")
        assert response.status_code in [404, 500]
    
    def test_invalid_audience_description(self, client):
        """Test persona generation with invalid input"""
        response = client.post(
            "/api/personas/generate",
            json={"audience_description": "Hi"}  # Too short
        )
        
        assert response.status_code == 422  # Validation error


class TestDatabaseIntegrity:
    """Tests for database constraints and relationships"""
    
    def test_foreign_key_constraints(self, test_db, test_user):
        """Test that foreign keys are enforced"""
        from sqlalchemy.exc import IntegrityError
        
        # Try to create simulation result without draft
        result = SimulationResult(
            simulation_id="test-sim-err",
            draft_id=99999,  # Non-existent
            persona_id=1,
            internal_monologue="Test",
            public_comment="Test",
            trust_score=5,
            excitement_score=5,
            backlash_risk_score=5,
            reasoning="Test",
            status="success"
        )
        test_db.add(result)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_cascade_deletes(self, test_db, test_user):
        """Test cascade deletion of related records"""
        # Create draft with results
        draft = Draft(
            content="Test",
            user_id=test_user.id,
            persona_set_id="test"
        )
        test_db.add(draft)
        test_db.commit()
        test_db.refresh(draft)
        
        # Add persona
        persona = Persona(
            set_id="test",
            name="Test",
            archetype="Test",
            loyalty_level=5,
            core_values=["V1", "V2"],
            audience_description="Test",
            user_id=test_user.id
        )
        test_db.add(persona)
        test_db.commit()
        test_db.refresh(persona)
        
        # Add result
        result = SimulationResult(
            simulation_id="test-sim-123",
            draft_id=draft.id,
            persona_id=persona.id,
            internal_monologue="Test",
            public_comment="Test",
            trust_score=5,
            excitement_score=5,
            backlash_risk_score=5,
            reasoning="Test",
            status="success"
        )
        test_db.add(result)
        test_db.commit()
        
        # Delete draft
        test_db.delete(draft)
        test_db.commit()
        
        # Results should be deleted too (if cascade is configured)
        remaining = test_db.query(SimulationResult).filter(
            SimulationResult.draft_id == draft.id
        ).count()
        assert remaining == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
