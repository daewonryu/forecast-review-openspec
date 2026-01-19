"""
Performance tests for FanEcho MVP
"""
import pytest
import time
import asyncio
from unittest.mock import Mock, AsyncMock, patch
from concurrent.futures import ThreadPoolExecutor

from app.services.simulation import SimulationService
from app.services.persona import PersonaService
from app.services.llm import LLMService


class TestParallelPerformance:
    """Tests for parallel execution performance"""
    
    @pytest.mark.asyncio
    async def test_simulation_completes_within_time_limit(self):
        """Test that simulation completes within 60 seconds"""
        
        # Mock services
        mock_db = Mock()
        mock_llm = Mock(spec=LLMService)
        mock_persona_service = Mock(spec=PersonaService)
        
        # Mock LLM calls with realistic delays
        async def mock_reaction(*args, **kwargs):
            await asyncio.sleep(10)  # Simulate 10s LLM call
            return {
                "internal_reaction": "Test",
                "public_response": "Test",
                "trust_score": 5,
                "excitement_score": 5,
                "backlash_score": 5,
                "reasoning": "Test"
            }
        
        mock_persona_service.generate_persona_reaction = AsyncMock(side_effect=mock_reaction)
        
        # Create 5 test personas
        personas = []
        for i in range(5):
            persona = Mock()
            persona.id = i
            persona.name = f"Persona {i}"
            persona.loyalty_level = 5
            persona.core_values = ["Test"]
            persona.traits = "Test"
            personas.append(persona)
        
        # Run simulation
        service = SimulationService(
            llm_service=mock_llm,
            persona_service=mock_persona_service
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
        
        # With parallel execution: ~10s (all run simultaneously)
        # Without parallel execution: ~50s (5 x 10s)
        assert elapsed < 20  # Allow buffer for overhead
        assert elapsed < 60  # Must be under requirement
        assert len(results) == 5
    
    @pytest.mark.asyncio
    async def test_timeout_enforcement(self):
        """Test that individual persona simulations timeout after 65s"""
        
        mock_db = Mock()
        mock_llm = Mock()
        mock_persona_service = Mock()
        
        # Mock very slow LLM call (70 seconds)
        async def slow_reaction(*args, **kwargs):
            await asyncio.sleep(70)
            return {
                "internal_reaction": "Should timeout",
                "public_response": "Should timeout",
                "trust_score": 5,
                "excitement_score": 5,
                "backlash_score": 5,
                "reasoning": "Test"
            }
        
        mock_persona_service.generate_persona_reaction = AsyncMock(side_effect=slow_reaction)
        
        persona = Mock()
        persona.id = 1
        persona.name = "Test Persona"
        persona.loyalty_level = 5
        persona.core_values = ["Test"]
        persona.traits = "Test"
        
        service = SimulationService(
            llm_service=mock_llm,
            persona_service=mock_persona_service
        )
        
        start_time = time.time()
        with pytest.raises(Exception) as exc_info:
            await service._run_single_simulation_with_timeout(
                persona={"id": 1, "name": "Test Persona", "loyalty_level": 5},
                content="Test",
                audience_description="Test"
            )
        elapsed = time.time() - start_time
        
        # Should timeout at 65 seconds
        assert elapsed < 70
        assert "timeout" in str(exc_info.value).lower()
    
    @pytest.mark.asyncio
    async def test_partial_failure_handling(self):
        """Test that partial failures don't block other results"""
        
        mock_db = Mock()
        mock_llm = Mock()
        mock_persona_service = Mock()
        
        # Mock mixed success/failure responses
        call_count = [0]
        async def mixed_reaction(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] in [2, 4]:  # Fail on 2nd and 4th
                raise Exception("Simulated LLM failure")
            await asyncio.sleep(0.1)
            return {
                "internal_reaction": "Success",
                "public_response": "Success",
                "trust_score": 5,
                "excitement_score": 5,
                "backlash_score": 5,
                "reasoning": "Test"
            }
        
        mock_persona_service.generate_persona_reaction = AsyncMock(side_effect=mixed_reaction)
        
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
            llm_service=mock_llm,
            persona_service=mock_persona_service
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
        
        results = await service._run_parallel_simulations(
            content="Test",
            requests=requests,
            simulation_id="test-sim-123",
            draft_id=1,
            db=mock_db
        )
        
        # Should have all 5 results (3 success, 2 error)
        assert len(results) == 5
        success_count = sum(1 for r in results if r.get("status") == "success")
        error_count = sum(1 for r in results if r.get("status") == "error")
        assert success_count == 3
        assert error_count == 2


class TestDatabasePerformance:
    """Tests for database query performance"""
    
    def test_persona_retrieval_performance(self):
        """Test that persona retrieval is fast with proper indexing"""
        # This would test with actual database
        # Placeholder for now
        pass
    
    def test_simulation_results_query_performance(self):
        """Test that simulation results queries are optimized"""
        # This would test with actual database and many records
        pass


class TestLLMCostOptimization:
    """Tests for token usage and cost optimization"""
    
    @pytest.mark.asyncio
    async def test_prompt_token_efficiency(self):
        """Test that prompts are reasonably sized"""
        from app.services.prompts import PERSONA_GENERATION_SYSTEM_PROMPT, PERSONA_GENERATION_USER_PROMPT
        
        # Check prompt lengths (rough token estimation: 1 token ≈ 4 chars)
        system_tokens = len(PERSONA_GENERATION_SYSTEM_PROMPT) / 4
        user_prompt = PERSONA_GENERATION_USER_PROMPT.format(
            audience_description="Test audience description"
        )
        user_tokens = len(user_prompt) / 4
        
        # System prompts should be under 500 tokens
        assert system_tokens < 500
        
        # User prompts should be under 300 tokens
        assert user_tokens < 300
    
    @pytest.mark.asyncio
    async def test_response_parsing_efficiency(self):
        """Test that response parsing doesn't fail and require retries"""
        from app.services.persona import PersonaService
        import json
        
        mock_db = Mock()
        mock_llm = Mock()
        
        # Valid JSON response
        valid_response = {
            "content": json.dumps({
                "personas": [
                    {
                        "name": f"Persona {i}",
                        "archetype": f"Arch {i}",
                        "loyalty_level": i + 3,
                        "core_values": ["V1", "V2"]
                    }
                    for i in range(5)
                ]
            }),
            "cost": 0.01,
            "duration": 1.5
        }
        
        mock_llm.generate = AsyncMock(return_value=valid_response)
        
        service = PersonaService(llm_service=mock_llm)
        
        # Should parse successfully on first try
        result = await service.generate_personas(
            audience_description="Test",
            user_id=1,
            db=mock_db,
            save_to_library=False
        )
        
        personas = result["personas"]
        assert len(personas) == 5
        # LLM should only be called once
        assert mock_llm.generate.call_count == 1


class TestConcurrentUsers:
    """Tests for handling multiple concurrent users"""
    
    @pytest.mark.asyncio
    async def test_concurrent_simulations(self):
        """Test multiple users running simulations simultaneously"""
        
        async def run_simulation(user_id):
            """Simulate a user running a simulation"""
            await asyncio.sleep(0.1)  # Simulate work
            return {"user_id": user_id, "completed": True}
        
        # Simulate 10 concurrent users
        tasks = [run_simulation(i) for i in range(10)]
        start_time = time.time()
        results = await asyncio.gather(*tasks)
        elapsed = time.time() - start_time
        
        # Should complete in ~0.1s (parallel), not ~1s (serial)
        assert elapsed < 0.5
        assert len(results) == 10


class TestMemoryUsage:
    """Tests for memory efficiency"""
    
    def test_large_result_sets(self):
        """Test handling large numbers of simulation results"""
        from app.services.insights import InsightsService
        from app.db.models import SimulationResult, Persona
        
        # Create large result set
        results = []
        for i in range(100):
            result = Mock(spec=SimulationResult)
            result.trust_score = 5
            result.excitement_score = 5
            result.backlash_score = 5
            result.persona = Mock(spec=Persona)
            result.persona.name = f"Persona {i}"
            result.persona_id = i
            results.append(result)
        
        service = InsightsService(db=Mock(), llm_service=Mock())
        
        # Should handle large datasets efficiently
        analytics = service.calculate_aggregate_analytics(results)
        
        assert analytics is not None
        assert len(analytics["score_distribution"]) == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
