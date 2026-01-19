"""
LLM service abstraction layer
Handles communication with OpenAI and Anthropic APIs with retry logic and fallback
"""
import asyncio
import logging
import time
from typing import Optional, Dict, Any, List
from enum import Enum
import json

from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type
)

from app.config import settings

logger = logging.getLogger(__name__)


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class LLMServiceError(Exception):
    """Custom exception for LLM service errors"""
    pass


class LLMService:
    """
    Unified LLM service supporting OpenAI and Anthropic with:
    - Retry logic with exponential backoff
    - Timeout handling
    - Cost tracking
    - Provider fallback
    """
    
    def __init__(self):
        self.openai_client = None
        self.anthropic_client = None
        self.primary_provider = LLMProvider(settings.PRIMARY_LLM_PROVIDER)
        self.timeout = settings.LLM_TIMEOUT
        self.max_retries = settings.LLM_MAX_RETRIES
        self.temperature = settings.LLM_TEMPERATURE
        
        # Cost tracking
        self.total_cost = 0.0
        self.request_count = 0
        
        # Initialize clients
        self._init_clients()
    
    def _init_clients(self):
        """Initialize LLM API clients"""
        if settings.OPENAI_API_KEY:
            self.openai_client = AsyncOpenAI(
                api_key=settings.OPENAI_API_KEY,
                timeout=self.timeout
            )
            logger.info("OpenAI client initialized")
        else:
            logger.warning("OpenAI API key not configured")
        
        # if settings.ANTHROPIC_API_KEY:
        #     self.anthropic_client = AsyncAnthropic(
        #         api_key=settings.ANTHROPIC_API_KEY,
        #         timeout=self.timeout
        #     )
        #     logger.info("Anthropic client initialized")
        # else:
        #     logger.warning("Anthropic API key not configured")
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def _call_openai(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        **kwargs
    ) -> Dict[str, Any]:
        """Call OpenAI API with retry logic"""
        if not self.openai_client:
            raise LLMServiceError("OpenAI client not initialized")
        
        try:
            start_time = time.time()
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=kwargs.get('temperature', self.temperature),
                max_tokens=kwargs.get('max_tokens', 2000),
            )
            duration = time.time() - start_time
            
            # Track usage
            self.request_count += 1
            estimated_cost = self._estimate_openai_cost(response.usage, model)
            self.total_cost += estimated_cost
            
            logger.info(
                f"OpenAI API call successful - "
                f"Model: {model}, Duration: {duration:.2f}s, "
                f"Tokens: {response.usage.total_tokens}, "
                f"Cost: ${estimated_cost:.4f}"
            )
            
            return {
                "content": response.choices[0].message.content,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                },
                "cost": estimated_cost,
                "duration": duration
            }
        
        except asyncio.TimeoutError:
            logger.error(f"OpenAI API timeout after {self.timeout}s")
            raise LLMServiceError(f"OpenAI API timeout after {self.timeout}s")
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    @retry(
        stop=stop_after_attempt(2),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
        reraise=True
    )
    async def _call_anthropic(
        self,
        messages: List[Dict[str, str]],
        model: str = "claude-3-5-sonnet-20241022",
        **kwargs
    ) -> Dict[str, Any]:
        """Call Anthropic API with retry logic"""
        if not self.anthropic_client:
            raise LLMServiceError("Anthropic client not initialized")
        
        try:
            start_time = time.time()
            
            # Convert messages format for Anthropic
            system_message = None
            anthropic_messages = []
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    anthropic_messages.append(msg)
            
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=kwargs.get('max_tokens', 2000),
                temperature=kwargs.get('temperature', self.temperature),
                system=system_message,
                messages=anthropic_messages
            )
            duration = time.time() - start_time
            
            # Track usage
            self.request_count += 1
            estimated_cost = self._estimate_anthropic_cost(response.usage, model)
            self.total_cost += estimated_cost
            
            logger.info(
                f"Anthropic API call successful - "
                f"Model: {model}, Duration: {duration:.2f}s, "
                f"Tokens: {response.usage.input_tokens + response.usage.output_tokens}, "
                f"Cost: ${estimated_cost:.4f}"
            )
            
            return {
                "content": response.content[0].text,
                "model": model,
                "usage": {
                    "prompt_tokens": response.usage.input_tokens,
                    "completion_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                },
                "cost": estimated_cost,
                "duration": duration
            }
        
        except asyncio.TimeoutError:
            logger.error(f"Anthropic API timeout after {self.timeout}s")
            raise LLMServiceError(f"Anthropic API timeout after {self.timeout}s")
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def generate(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[LLMProvider] = None,
        use_fallback: bool = True,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate response from LLM with fallback support
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            provider: Specific provider to use (defaults to primary)
            use_fallback: Whether to fallback to alternate provider on failure
            **kwargs: Additional arguments passed to LLM API
        
        Returns:
            Dictionary with response content and metadata
        """
        provider = provider or self.primary_provider
        
        try:
            if provider == LLMProvider.OPENAI:
                return await self._call_openai(messages, **kwargs)
            else:
                return await self._call_anthropic(messages, **kwargs)
        
        except Exception as e:
            logger.error(f"Primary provider {provider} failed: {e}")
            
            if use_fallback:
                # Try alternate provider
                fallback_provider = (
                    LLMProvider.ANTHROPIC if provider == LLMProvider.OPENAI
                    else LLMProvider.OPENAI
                )
                logger.info(f"Attempting fallback to {fallback_provider}")
                
                try:
                    if fallback_provider == LLMProvider.OPENAI:
                        return await self._call_openai(messages, **kwargs)
                    else:
                        return await self._call_anthropic(messages, **kwargs)
                except Exception as fallback_error:
                    logger.error(f"Fallback provider {fallback_provider} also failed: {fallback_error}")
                    raise LLMServiceError(
                        f"Both primary ({provider}) and fallback ({fallback_provider}) providers failed"
                    )
            else:
                raise LLMServiceError(f"LLM provider {provider} failed: {str(e)}")
    
    async def generate_parallel(
        self,
        requests: List[Dict[str, Any]],
        provider: Optional[LLMProvider] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple responses in parallel
        
        Args:
            requests: List of request dictionaries, each with 'messages' and optional kwargs
            provider: Provider to use for all requests
        
        Returns:
            List of response dictionaries (may include errors)
        """
        tasks = [
            self.generate(
                messages=req["messages"],
                provider=provider,
                use_fallback=req.get("use_fallback", True),
                **req.get("kwargs", {})
            )
            for req in requests
        ]
        
        # Use gather with return_exceptions to handle partial failures
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Convert exceptions to error dictionaries
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                processed_results.append({
                    "error": str(result),
                    "status": "error",
                    "request_index": i
                })
            else:
                processed_results.append({
                    **result,
                    "status": "success",
                    "request_index": i
                })
        
        return processed_results
    
    def _estimate_openai_cost(self, usage: Any, model: str) -> float:
        """Estimate cost for OpenAI API call"""
        # Pricing as of Jan 2026 (approximate)
        pricing = {
            "gpt-4o": {"input": 0.005, "output": 0.015},  # per 1K tokens
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        }
        
        model_pricing = pricing.get(model, pricing["gpt-4o"])
        input_cost = (usage.prompt_tokens / 1000) * model_pricing["input"]
        output_cost = (usage.completion_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def _estimate_anthropic_cost(self, usage: Any, model: str) -> float:
        """Estimate cost for Anthropic API call"""
        # Pricing as of Jan 2026 (approximate)
        pricing = {
            "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},  # per 1K tokens
        }
        
        model_pricing = pricing.get(model, pricing["claude-3-5-sonnet-20241022"])
        input_cost = (usage.input_tokens / 1000) * model_pricing["input"]
        output_cost = (usage.output_tokens / 1000) * model_pricing["output"]
        
        return input_cost + output_cost
    
    def get_stats(self) -> Dict[str, Any]:
        """Get service statistics"""
        return {
            "total_requests": self.request_count,
            "total_cost": round(self.total_cost, 4),
            "primary_provider": self.primary_provider.value,
            "openai_available": self.openai_client is not None,
            "anthropic_available": self.anthropic_client is not None
        }


# Global LLM service instance
llm_service = LLMService()


# Dependency for FastAPI
def get_llm_service() -> LLMService:
    """Dependency function to get LLM service"""
    return llm_service
