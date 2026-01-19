"""
Unit tests for FanEcho MVP
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import json

# Test fixtures
@pytest.fixture
def mock_db():
    """Mock database session"""
    return Mock()


@pytest.fixture
def mock_llm_service():
    """Mock LLM service"""
    service = Mock()
    service.generate = AsyncMock()
    return service


# Persona Service Tests
class TestPersonaService:
    """Tests for persona generation and management"""
    
    @pytest.mark.asyncio
    async def test_generate_personas_success(self, mock_db, mock_llm_service):
        """Test successful persona generation"""
        from app.services.persona import PersonaService
        
        # Mock LLM response
        mock_llm_service.generate.return_value = {
            "content": json.dumps({
                "personas": [
                    {
                        "name": "The Veteran",
                        "archetype": "Long-time supporter",
                        "loyalty_level": 9,
                        "core_values": ["Nostalgia", "Community"]
                    },
                    {
                        "name": "The Skeptic",
                        "archetype": "Critical observer",
                        "loyalty_level": 3,
                        "core_values": ["Transparency", "Value"]
                    },
                    {
                        "name": "The Casual Fan",
                        "archetype": "Moderate supporter",
                        "loyalty_level": 5,
                        "core_values": ["Entertainment", "Accessibility"]
                    },
                    {
                        "name": "The Enthusiast",
                        "archetype": "Excited supporter",
                        "loyalty_level": 8,
                        "core_values": ["Innovation", "Exclusivity"]
                    },
                    {
                        "name": "The Newcomer",
                        "archetype": "New follower",
                        "loyalty_level": 4,
                        "core_values": ["Curiosity", "Welcoming"]
                    }
                ]
            }),
            "cost": 0.01,
            "duration": 1.5
        }
        
        service = PersonaService(llm_service=mock_llm_service)
        result = await service.generate_personas(
            audience_description="Tech enthusiasts interested in AI",
            user_id=1,
            db=mock_db,
            save_to_library=False
        )
        
        personas = result["personas"]
        assert len(personas) == 5
        assert personas[0]["name"] == "The Veteran"
        assert personas[0]["loyalty_level"] == 9
        assert len(personas[0]["core_values"]) >= 2
        
        # Verify LLM was called
        mock_llm_service.generate.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_generate_personas_diversity(self, mock_db, mock_llm_service):
        """Test that personas have diverse loyalty levels"""
        from app.services.persona import PersonaService
        
        mock_llm_service.generate.return_value = {
            "content": json.dumps({
                "personas": [
                    {"name": "P1", "archetype": "A1", "loyalty_level": 9, "core_values": ["V1", "V2"]},
                    {"name": "P2", "archetype": "A2", "loyalty_level": 7, "core_values": ["V3", "V4"]},
                    {"name": "P3", "archetype": "A3", "loyalty_level": 5, "core_values": ["V5", "V6"]},
                    {"name": "P4", "archetype": "A4", "loyalty_level": 3, "core_values": ["V7", "V8"]},
                    {"name": "P5", "archetype": "A5", "loyalty_level": 2, "core_values": ["V9", "V10"]}
                ]
            }),
            "cost": 0.01,
            "duration": 1.5
        }
        
        service = PersonaService(llm_service=mock_llm_service)
        result = await service.generate_personas(
            audience_description="Test audience",
            user_id=1,
            db=mock_db,
            save_to_library=False
        )
        
        personas = result["personas"]
        loyalty_levels = [p["loyalty_level"] for p in personas]
        
        # Should have both high and low loyalty
        assert max(loyalty_levels) >= 7
        assert min(loyalty_levels) <= 4
        assert len(set(loyalty_levels)) >= 3  # At least 3 different levels
    
    @pytest.mark.asyncio
    async def test_generate_persona_reaction(self, mock_db, mock_llm_service):
        """Test generating a single persona reaction"""
        from app.services.persona import PersonaService
        
        mock_llm_service.generate.return_value = {
            "content": json.dumps({
                "internal_reaction": "This is concerning, feels like a cash grab.",
                "public_response": "Not sure about this direction...",
                "trust_score": 4,
                "excitement_score": 3,
                "backlash_score": 7,
                "reasoning": "The tone feels overly promotional without substance"
            }),
            "cost": 0.01,
            "duration": 1.0
        }
        
        persona = {
            "name": "The Skeptic",
            "loyalty_level": 3,
            "core_values": ["Transparency", "Value"],
            "traits": "Critical, analytical"
        }
        
        service = PersonaService(llm_service=mock_llm_service)
        reaction = await service.generate_persona_reaction(
            persona=persona,
            content="Exciting new product launch!",
            audience_description="Tech enthusiasts"
        )
        
        assert reaction["trust_score"] >= 1 and reaction["trust_score"] <= 10
        assert reaction["excitement_score"] >= 1 and reaction["excitement_score"] <= 10
        assert reaction["backlash_score"] >= 1 and reaction["backlash_score"] <= 10
        assert len(reaction["internal_reaction"]) > 0
        assert len(reaction["public_response"]) > 0


# Simulation Service Tests
class TestSimulationService:
    """Tests for simulation engine"""
    
    @pytest.mark.asyncio
    async def test_calculate_aggregate_scores(self):
        """Test aggregate score calculation"""
        from app.services.simulation import SimulationService
        
        # Create mock results as dicts (matching actual structure)
        results = [
            {
                "status": "success",
                "persona_id": i,
                "persona_name": f"Persona {i}",
                "scores": {
                    "trust": 5 + i,
                    "excitement": 4 + i,
                    "backlash_risk": 3 - (i * 0.5)
                },
                "internal_monologue": "Test",
                "public_comment": "Test",
                "reasoning": "Test"
            }
            for i in range(5)
        ]
        
        service = SimulationService(llm_service=Mock(), persona_service=Mock())
        
        aggregate = service._calculate_aggregate_scores(results)
        
        # Average trust: (5+6+7+8+9)/5 = 7.0
        assert aggregate.avg_trust == 7.0
        # Average excitement: (4+5+6+7+8)/5 = 6.0
        assert aggregate.avg_excitement == 6.0
        # Average backlash: (3+2.5+2+1.5+1)/5 = 2.0
        assert aggregate.avg_backlash_risk == 2.0
    
    @pytest.mark.asyncio
    async def test_parallel_simulation_execution(self, mock_db, mock_llm_service):
        """Test that simulations run in parallel"""
        from app.services.simulation import SimulationService
        from app.services.persona import PersonaService
        import time
        
        # Mock persona service
        persona_service = Mock(spec=PersonaService)
        
        async def mock_reaction(*args, **kwargs):
            await asyncio.sleep(0.1)  # Simulate LLM call
            return {
                "internal_reaction": "Test",
                "public_response": "Test",
                "trust_score": 5,
                "excitement_score": 5,
                "backlash_score": 5,
                "reasoning": "Test"
            }
        
        persona_service.generate_persona_reaction = AsyncMock(side_effect=mock_reaction)
        
        # Create mock personas
        personas = []
        for i in range(5):
            persona = Mock()
            persona.id = i
            persona.name = f"Persona {i}"
            persona.loyalty_level = 5
            persona.core_values = ["Test"]
            persona.traits = "Test"
            personas.append(persona)
        
        service = SimulationService(
            llm_service=mock_llm_service,
            persona_service=persona_service
        )
        
        # Prepare requests
        requests = []
        for persona in personas:
            requests.append({
                "persona": {
                    "id": persona.id,
                    "name": persona.name,
                    "archetype": "Test",
                    "loyalty_level": persona.loyalty_level,
                    "core_values": persona.core_values
                },
                "audience_description": "Test"
            })
        
        start_time = time.time()
        results = await service._run_parallel_simulations(
            content="Test draft",
            requests=requests,
            simulation_id="test-sim-123",
            draft_id=1,
            db=mock_db
        )
        elapsed = time.time() - start_time
        
        # With parallel execution, should take ~0.1s
        # With serial execution, would take ~0.5s
        assert elapsed < 0.3
        assert len(results) == 5


# Insights Service Tests
class TestInsightsService:
    """Tests for insights generation"""
    
    def test_calculate_aggregate_analytics(self, mock_db):
        """Test aggregate analytics calculation"""
        from app.services.insights import InsightsService
        from app.db.models import SimulationResult, Persona
        
        # Create mock results
        results = []
        for i in range(5):
            result = Mock(spec=SimulationResult)
            result.trust_score = 6
            result.excitement_score = 7
            result.backlash_score = 3
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona_id = i
            results.append(result)
        
        service = InsightsService(db=mock_db, llm_service=Mock())
        analytics = service.calculate_aggregate_analytics(results)
        
        assert analytics["average_scores"]["trust"] == 6.0
        assert analytics["average_scores"]["excitement"] == 7.0
        assert analytics["average_scores"]["backlash"] == 3.0
        assert analytics["overall_sentiment"] == "positive"
        assert len(analytics["score_distribution"]) == 5
    
    def test_sentiment_determination(self, mock_db):
        """Test sentiment categorization logic"""
        from app.services.insights import InsightsService
        from app.db.models import SimulationResult, Persona
        
        service = InsightsService(db=mock_db, llm_service=Mock())
        
        # Test positive sentiment
        results_positive = []
        for i in range(5):
            result = Mock(spec=SimulationResult)
            result.trust_score = 8
            result.excitement_score = 8
            result.backlash_score = 2
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona_id = i
            results_positive.append(result)
        
        analytics = service.calculate_aggregate_analytics(results_positive)
        assert analytics["overall_sentiment"] == "positive"
        
        # Test negative sentiment
        results_negative = []
        for i in range(5):
            result = Mock(spec=SimulationResult)
            result.trust_score = 3
            result.excitement_score = 3
            result.backlash_score = 8
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona_id = i
            results_negative.append(result)
        
        analytics = service.calculate_aggregate_analytics(results_negative)
        assert analytics["overall_sentiment"] == "negative"
    
    @pytest.mark.asyncio
    async def test_extract_pain_points(self, mock_db, mock_llm_service):
        """Test pain point extraction"""
        from app.services.insights import InsightsService
        from app.db.models import SimulationResult, Persona
        
        mock_llm_service.generate.return_value = json.dumps([
            {
                "text": "cash grab",
                "severity": "high",
                "affected_personas": ["The Skeptic", "The Veteran"],
                "reasoning": "Perceived as exploitative pricing"
            }
        ])
        
        results = []
        for i in range(2):
            result = Mock(spec=SimulationResult)
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona.loyalty_level = 5
            result.internal_reaction = "Feels like a cash grab"
            result.public_response = "Not impressed"
            result.trust_score = 3
            result.excitement_score = 2
            result.backlash_score = 8
            result.reasoning = "Too expensive"
            results.append(result)
        
        service = InsightsService(db=mock_db, llm_service=mock_llm_service)
        pain_points = await service.extract_pain_points(
            draft_content="Buy our new $999 product!",
            simulation_results=results
        )
        
        assert len(pain_points) > 0
        assert pain_points[0]["severity"] == "high"
    
    def test_persona_drill_down(self, mock_db):
        """Test persona drill-down view"""
        from app.services.insights import InsightsService
        from app.db.models import SimulationResult, Persona
        
        # Create 5 mock results with different scores
        results = []
        for i in range(5):
            result = Mock(spec=SimulationResult)
            result.persona_id = str(i)
            result.trust_score = 5 + i
            result.excitement_score = 5
            result.backlash_score = 3
            result.internal_reaction = "Test"
            result.public_response = "Test"
            result.reasoning = "Test"
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona.loyalty_level = 5
            result.persona.core_values = ["Test"]
            result.persona.traits = "Test"
            results.append(result)
        
        service = InsightsService(db=mock_db, llm_service=Mock())
        
        # Get drill-down for outlier (persona_id=4 has trust_score=9)
        drill_down = service.get_persona_drill_down(
            persona_id="4",
            simulation_results=results
        )
        
        assert drill_down["persona_details"]["id"] == "4"
        assert drill_down["persona_scores"]["trust"] == 9
        assert drill_down["delta"]["trust"] == 2.0  # 9 - 7 (average)
        assert drill_down["is_outlier"] == False  # Delta is exactly 2.0, not > 2


# API Endpoint Tests
class TestAPIEndpoints:
    """Tests for API endpoints"""
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] in ["ok", "degraded"]  # "ok" if DB connected, "degraded" if not
    
    @pytest.mark.asyncio
    async def test_generate_personas_endpoint(self):
        """Test persona generation endpoint"""
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        with patch('app.routers.personas.PersonaService') as MockService:
            mock_service = Mock()
            mock_service.generate_personas = AsyncMock(return_value=[
                {"name": "Test", "loyalty_level": 5, "core_values": ["V1", "V2"]}
            ])
            MockService.return_value = mock_service
            
            response = client.post(
                "/api/personas/generate",
                json={"audience_description": "Test audience"}
            )
            
            assert response.status_code == 200


# Input Validation Tests
class TestInputValidation:
    """Tests for input validation"""
    
    def test_audience_description_length(self):
        """Test audience description validation"""
        from app.schemas import PersonaGenerateRequest
        from pydantic import ValidationError
        
        # Too short
        with pytest.raises(ValidationError):
            PersonaGenerateRequest(audience_description="Hi")
        
        # Too long
        with pytest.raises(ValidationError):
            PersonaGenerateRequest(audience_description="x" * 600)
        
        # Valid
        request = PersonaGenerateRequest(audience_description="Valid audience description")
        assert request.audience_description == "Valid audience description"
    
    def test_draft_content_validation(self):
        """Test draft content validation"""
        from app.schemas import DraftCreate
        from pydantic import ValidationError
        
        # Too short
        with pytest.raises(ValidationError):
            DraftCreate(content="Hi")
        
        # Too long
        with pytest.raises(ValidationError):
            DraftCreate(content="x" * 6000)
        
        # Valid
        draft = DraftCreate(content="This is valid draft content.")
        assert len(draft.content) >= 10


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
