"""
Main UI module for Agentic Blog Generator
Contains the Streamlit UI logic and components
"""
import streamlit as st
from .styles import apply_custom_styles, render_header, render_footer
from .sidebar import render_sidebar
from .main_content import render_main_content, render_blog_output
from .config_loader import get_config


def render_ui():
    """Main function to render the entire Streamlit UI"""
    # Load configuration
    config = get_config()
    page_config = config.get_page_config()
    
    # Page configuration
    st.set_page_config(
        page_title=page_config['page_title'],
        page_icon=page_config['page_icon'],
        layout=page_config['layout']
    )
    
    # Apply custom styles
    apply_custom_styles()
    
    # Render header
    render_header()
    
    # Render sidebar and get configuration
    config = render_sidebar()
    
    # Render main content
    render_main_content(config)
    
    # Render blog output if available
    if 'blog_data' in st.session_state:
        render_blog_output()
    
    # Render footer
    render_footer()

