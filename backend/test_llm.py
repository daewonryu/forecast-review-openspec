"""
LLM service testing and examples
"""
import asyncio
from app.services.llm import llm_service, LLMProvider


async def test_openai():
    """Test OpenAI API connection"""
    print("Testing OpenAI...")
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."}
        ]
        result = await llm_service.generate(messages, provider=LLMProvider.OPENAI)
        print(f"✓ OpenAI Success: {result['content']}")
        print(f"  Cost: ${result['cost']:.4f}, Duration: {result['duration']:.2f}s")
        return True
    except Exception as e:
        print(f"✗ OpenAI Failed: {e}")
        return False


async def test_anthropic():
    """Test Anthropic API connection"""
    print("\nTesting Anthropic...")
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello in one sentence."}
        ]
        result = await llm_service.generate(messages, provider=LLMProvider.ANTHROPIC)
        print(f"✓ Anthropic Success: {result['content']}")
        print(f"  Cost: ${result['cost']:.4f}, Duration: {result['duration']:.2f}s")
        return True
    except Exception as e:
        print(f"✗ Anthropic Failed: {e}")
        return False


async def test_fallback():
    """Test fallback logic"""
    print("\nTesting Fallback Logic...")
    try:
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Count to 3."}
        ]
        # Will use primary provider, fallback if needed
        result = await llm_service.generate(messages, use_fallback=True)
        print(f"✓ Fallback Test Success: {result['content']}")
        print(f"  Model: {result['model']}")
        return True
    except Exception as e:
        print(f"✗ Fallback Test Failed: {e}")
        return False


async def test_parallel():
    """Test parallel requests"""
    print("\nTesting Parallel Requests...")
    try:
        requests = [
            {
                "messages": [
                    {"role": "user", "content": f"What is {i} + {i}?"}
                ]
            }
            for i in range(3)
        ]
        
        start = asyncio.get_event_loop().time()
        results = await llm_service.generate_parallel(requests)
        duration = asyncio.get_event_loop().time() - start
        
        successful = sum(1 for r in results if r.get("status") == "success")
        print(f"✓ Parallel Test: {successful}/{len(requests)} succeeded in {duration:.2f}s")
        
        for i, result in enumerate(results):
            if result.get("status") == "success":
                print(f"  Request {i}: {result['content'][:50]}...")
            else:
                print(f"  Request {i}: Error - {result.get('error')}")
        
        return successful > 0
    except Exception as e:
        print(f"✗ Parallel Test Failed: {e}")
        return False


async def main():
    """Run all tests"""
    print("=" * 60)
    print("LLM Service Test Suite")
    print("=" * 60)
    
    tests = [
        ("OpenAI", test_openai),
        ("Anthropic", test_anthropic),
        ("Fallback", test_fallback),
        ("Parallel", test_parallel),
    ]
    
    results = []
    for name, test_func in tests:
        result = await test_func()
        results.append((name, result))
    
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {name}")
    
    print("\nService Stats:")
    stats = llm_service.get_stats()
    print(f"  Total Requests: {stats['total_requests']}")
    print(f"  Total Cost: ${stats['total_cost']}")
    print(f"  Primary Provider: {stats['primary_provider']}")
    print(f"  OpenAI Available: {stats['openai_available']}")
    print(f"  Anthropic Available: {stats['anthropic_available']}")


if __name__ == "__main__":
    asyncio.run(main())
