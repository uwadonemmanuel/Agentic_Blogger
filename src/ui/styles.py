"""
UI Styles and CSS for Streamlit app
"""
import streamlit as st
from .config_loader import get_config

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .blog-content {
            background-color: #f0f2f6;
            padding: 1.5rem;
            border-radius: 10px;
            margin-top: 1rem;
        }
        .stButton>button {
            width: 100%;
            background-color: #1f77b4;
            color: white;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the main header"""
    config = get_config()
    header_text = config.get_ui_text('HEADER_TITLE', '📝 Agentic Blog Generator')
    st.markdown(f'<h1 class="main-header">{header_text}</h1>', unsafe_allow_html=True)

def render_footer():
    """Render the footer"""
    config = get_config()
    footer_text = config.get_ui_text('FOOTER_TEXT', 'Powered by LangGraph, FastAPI, and OpenAI')
    st.divider()
    st.markdown(f"""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>{footer_text}</p>
    </div>
    """, unsafe_allow_html=True)

