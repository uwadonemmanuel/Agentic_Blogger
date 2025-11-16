"""
LLM Factory for OpenAI models only
"""
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
from typing import Optional
from enum import Enum

load_dotenv()

class LLMProvider(str, Enum):
    """Supported LLM providers"""
    OPENAI = "openai"

class LLMModel(str, Enum):
    """Available OpenAI LLM models (as of November 2025)"""
    # OpenAI models - GPT-5 series (latest, released August 2025)
    OPENAI_GPT_5 = "gpt-5"
    OPENAI_GPT_5_MINI = "gpt-5-mini"
    
    # OpenAI models - GPT-4.1 series (released April 2025)
    OPENAI_GPT_41 = "gpt-4.1"
    OPENAI_GPT_41_MINI = "gpt-4.1-mini"
    OPENAI_GPT_41_NANO = "gpt-4.1-nano"
    
    # OpenAI models - GPT-4o series (current, reinstated for paid subscribers)
    OPENAI_GPT_4O = "gpt-4o"
    OPENAI_GPT_4O_MINI = "gpt-4o-mini"
    
    # OpenAI models - GPT-3.5 series (current version)
    OPENAI_GPT_35_TURBO = "gpt-3.5-turbo"

# Model to provider mapping
MODEL_PROVIDER_MAP = {
    # OpenAI models - GPT-5 series
    LLMModel.OPENAI_GPT_5: LLMProvider.OPENAI,
    LLMModel.OPENAI_GPT_5_MINI: LLMProvider.OPENAI,
    
    # OpenAI models - GPT-4.1 series
    LLMModel.OPENAI_GPT_41: LLMProvider.OPENAI,
    LLMModel.OPENAI_GPT_41_MINI: LLMProvider.OPENAI,
    LLMModel.OPENAI_GPT_41_NANO: LLMProvider.OPENAI,
    
    # OpenAI models - GPT-4o series
    LLMModel.OPENAI_GPT_4O: LLMProvider.OPENAI,
    LLMModel.OPENAI_GPT_4O_MINI: LLMProvider.OPENAI,
    
    # OpenAI models - GPT-3.5 series
    LLMModel.OPENAI_GPT_35_TURBO: LLMProvider.OPENAI,
}

# Human-readable model names
MODEL_DISPLAY_NAMES = {
    # OpenAI - GPT-5 series (Latest Generation, released Aug 2025)
    LLMModel.OPENAI_GPT_5: "GPT-5  - Latest Generation ⭐",
    LLMModel.OPENAI_GPT_5_MINI: "GPT-5 Mini  - Fast & Latest",
    
    # OpenAI - GPT-4.1 series (Released April 2025)
    LLMModel.OPENAI_GPT_41: "GPT-4.1  - Enhanced Coding & Long Context",
    LLMModel.OPENAI_GPT_41_MINI: "GPT-4.1 Mini  - Fast & Efficient",
    LLMModel.OPENAI_GPT_41_NANO: "GPT-4.1 Nano  - Lightweight",
    
    # OpenAI - GPT-4o series (Reinstated for paid subscribers)
    LLMModel.OPENAI_GPT_4O: "GPT-4o  - High Quality",
    LLMModel.OPENAI_GPT_4O_MINI: "GPT-4o Mini  - Fast & Efficient",
    
    # OpenAI - GPT-3.5 series
    LLMModel.OPENAI_GPT_35_TURBO: "GPT-3.5 Turbo  - Fast & Cost-Effective",
}

class LLMFactory:
    """Factory class for creating LLM instances"""
    
    @staticmethod
    def get_llm(
        model: str = LLMModel.OPENAI_GPT_4O.value,
        provider: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ):
        """
        Get an LLM instance based on model name
        
        Args:
            model: Model name (e.g., 'gpt-4o', 'gpt-5', 'gpt-4.1')
            provider: Provider name (optional, defaults to 'openai'). Only OpenAI is supported.
            temperature: Temperature for generation
            **kwargs: Additional model-specific parameters
            
        Returns:
            LLM instance (ChatOpenAI)
        """
        # Only OpenAI is supported
        if provider and provider.lower() != "openai":
            raise ValueError(f"Unsupported provider: {provider}. Only OpenAI is supported.")
        
        return LLMFactory._get_openai_llm(model, temperature, **kwargs)
    
    @staticmethod
    def _get_openai_llm(model: str, temperature: float, **kwargs):
        """Create an OpenAI LLM instance"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # All current OpenAI models support temperature parameter
        llm_kwargs = {
            "api_key": api_key,
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        
        return ChatOpenAI(**llm_kwargs)
    
    @staticmethod
    def get_available_models(provider: Optional[str] = None):
        """Get list of available OpenAI models"""
        # Only OpenAI models are available
        return [model.value for model in LLMModel]
    
    @staticmethod
    def get_model_display_name(model: str) -> str:
        """Get human-readable name for a model"""
        try:
            model_enum = LLMModel(model)
            return MODEL_DISPLAY_NAMES.get(model_enum, model)
        except ValueError:
            return model

