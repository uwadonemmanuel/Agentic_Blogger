"""
Sidebar component for Streamlit UI
Handles configuration and LLM settings
"""
import streamlit as st
import requests
from typing import Dict, Optional
from src.llms.llm_factory import MODEL_DISPLAY_NAMES, LLMModel
from .config_loader import get_config


def render_sidebar() -> Dict:
    """
    Render the sidebar with configuration options
    
    Returns:
        Dictionary containing configuration (api_url, model, temperature, etc.)
    """
    ui_config = get_config()
    api_config = ui_config.get_api_config()
    
    with st.sidebar:
        st.header(ui_config.get_ui_text('SIDEBAR_CONFIG_HEADER', '⚙️ Configuration'))
        
        # API endpoint configuration
        api_url = st.text_input(
            "API Endpoint",
            value=api_config['endpoint'],
            help="URL of the FastAPI backend"
        )
        
        st.divider()
        
        st.header(ui_config.get_ui_text('SIDEBAR_LLM_HEADER', '🤖 LLM Settings'))
        
        # Fetch available models from API
        llm_config = _get_llm_configuration(api_url, ui_config)
        
        st.divider()
        
        st.header(ui_config.get_ui_text('SIDEBAR_ABOUT_HEADER', 'ℹ️ About'))
        
        # Build about content from config
        about_content = ui_config.get_ui_text('ABOUT_CONTENT', 'This app uses LangGraph to generate blog posts with:')
        features = [
            ui_config.get_ui_text('ABOUT_FEATURE_1', '**Topic-based generation**: Create blogs on any topic'),
            ui_config.get_ui_text('ABOUT_FEATURE_2', '**Multi-language support**: Translate to multiple languages'),
                   ui_config.get_ui_text('ABOUT_FEATURE_3', '**OpenAI models**: Latest GPT models including GPT-5, GPT-4.1, and GPT-4o series'),
            ui_config.get_ui_text('ABOUT_FEATURE_4', '**Customizable settings**: Adjust temperature and model selection')
        ]
        
        about_markdown = about_content + '\n' + '\n'.join(f'- {feature}' for feature in features)
        st.markdown(about_markdown)
    
    return {
        "api_url": api_url,
        "model_id": llm_config["model_id"],
        "model_display": llm_config["model_display"],
        "temperature": llm_config["temperature"],
        "model_info": llm_config["model_info"]
    }


def _get_llm_configuration(api_url: str, ui_config) -> Dict:
    """Get LLM configuration from API or fallback"""
    models_api_url = api_url.replace("/blogs", "/models")
    available_models = []
    model_display_map = {}
    
    try:
        models_response = requests.get(models_api_url, timeout=5)
        if models_response.status_code == 200:
            models_data = models_response.json()
            available_models = models_data.get("models", [])
            model_display_map = {m["name"]: m["id"] for m in available_models}
    except:
        # Fallback to default models if API is not available
        available_models = [
            {
                "id": model.value,
                "name": MODEL_DISPLAY_NAMES.get(model, model.value),
                "provider": "openai"
            }
            for model in LLMModel
        ]
        model_display_map = {m["name"]: m["id"] for m in available_models}
    
    # Model selection
    selected_model_display = st.selectbox(
        "Select LLM Model",
        options=[m["name"] for m in available_models],
        index=0,
        help="Choose the LLM model to use for blog generation"
    )
    
    selected_model_id = model_display_map.get(
        selected_model_display,
        available_models[0]["id"] if available_models else "gpt-4o"
    )
    
    # Temperature slider - use config values
    llm_defaults = ui_config.get_llm_config()
    temperature = st.slider(
        "Temperature",
        min_value=llm_defaults['temperature_min'],
        max_value=llm_defaults['temperature_max'],
        value=llm_defaults['default_temperature'],
        step=llm_defaults['temperature_step'],
        help="Controls randomness. Lower = more focused, Higher = more creative"
    )
    
    # Show model info
    selected_model_info = next(
        (m for m in available_models if m["id"] == selected_model_id),
        None
    )
    if selected_model_info:
        st.info(f"🧠 **Provider**: {selected_model_info['provider'].upper()}")
    
    return {
        "model_id": selected_model_id,
        "model_display": selected_model_display,
        "temperature": temperature,
        "model_info": selected_model_info
    }

