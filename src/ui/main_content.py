"""
Main content components for Streamlit UI
Handles blog input, generation, and output display
"""
import streamlit as st
import requests
from typing import Dict, Optional
from .config_loader import get_config


def render_main_content(config: Dict):
    """
    Render the main content area with blog input form
    
    Args:
        config: Configuration dictionary from sidebar
    """
    ui_config = get_config()
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Blog Input")
        
        topic = st.text_input(
            "Blog Topic",
            placeholder=ui_config.get_ui_text('BLOG_INPUT_PLACEHOLDER', 'e.g., Artificial Intelligence, Python Programming, etc.'),
            help="Enter the topic for your blog post"
        )
        
        # Get languages from config
        languages = [""] + ui_config.get_languages()
        language = st.selectbox(
            "Translation Language (Optional)",
            options=languages,
            format_func=lambda x: {
                "": "English (Default)",
                "hindi": "Hindi (हिंदी)",
                "french": "French (Français)",
                "hausa": "Hausa",
                "yoruba": "Yoruba",
                "igbo": "Igbo"
            }.get(x, x),
            help="Select a language to translate the blog. Leave empty for English only."
        )
        
        generate_button = st.button(
            ui_config.get_ui_text('GENERATE_BUTTON_TEXT', '🚀 Generate Blog'),
            type="primary",
            use_container_width=True
        )
    
    with col2:
        st.header("📊 Status")
        
        if 'blog_data' in st.session_state:
            st.success("✅ Blog generated successfully!")
            st.json(st.session_state.get('blog_metadata', {}))
    
    # Handle blog generation
    if generate_button:
        _handle_blog_generation(topic, language, config)


def _handle_blog_generation(topic: str, language: str, config: Dict):
    """Handle blog generation request"""
    ui_config = get_config()
    api_config = ui_config.get_api_config()
    
    if not topic:
        st.error("❌ Please enter a blog topic!")
        return
    
    with st.spinner("🔄 Generating your blog... This may take a moment."):
        try:
            # Prepare request data
            payload = {
                "topic": topic,
                "language": language if language else "",
                "model": config["model_id"],
                "temperature": config["temperature"]
            }
            
            # Make API request
            response = requests.post(
                config["api_url"],
                json=payload,
                timeout=api_config['timeout']
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Validate response format
                if not isinstance(data, dict):
                    st.error(f"❌ Unexpected response format. Expected dict, got {type(data)}")
                    st.json(data)
                    return
                
                # Check for errors in successful response
                if 'error' in data:
                    st.error(f"❌ Error: {data.get('error', 'Unknown error')}")
                    if 'message' in data:
                        st.info(data['message'])
                    return
                
                st.session_state['blog_data'] = data
                st.session_state['blog_metadata'] = {
                    "topic": topic,
                    "language": language if language else "English",
                    "model": config["model_display"],
                    "temperature": config["temperature"],
                    "status": "success"
                }
                
                # Show model used in response
                if "model_used" in data:
                    st.session_state['blog_metadata']["model_used"] = data.get("model_used")
                st.rerun()
            else:
                st.error(f"❌ Error: {response.status_code}")
                try:
                    error_data = response.json()
                    st.json(error_data)
                    # Store error in session state for debugging
                    st.session_state['blog_data'] = error_data
                except:
                    st.text(response.text)
                
        except requests.exceptions.ConnectionError:
            st.error("❌ Could not connect to the API. Make sure the FastAPI server is running on port 8000.")
            st.info("💡 Run: `python app.py` to start the server")
        except requests.exceptions.Timeout:
            st.error("❌ Request timed out. The blog generation is taking longer than expected.")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")


def render_blog_output():
    """Render the generated blog output"""
    st.divider()
    st.header("📄 Generated Blog")
    
    # Safely get blog_data from session state
    blog_data_raw = st.session_state.get('blog_data', {})
    
    # Handle case where blog_data might be a list or dict
    if isinstance(blog_data_raw, list):
        st.error("❌ Unexpected response format from API. Please try again.")
        st.json(blog_data_raw)
        return
    
    if not isinstance(blog_data_raw, dict):
        st.error(f"❌ Unexpected data type: {type(blog_data_raw)}. Expected dict.")
        return
    
    # Check for errors in response
    if 'error' in blog_data_raw:
        st.error(f"❌ Error: {blog_data_raw.get('error', 'Unknown error')}")
        if 'message' in blog_data_raw:
            st.info(blog_data_raw['message'])
        return
    
    # Get the data field
    blog_data = blog_data_raw.get('data', {})
    
    if not isinstance(blog_data, dict):
        st.error("❌ Invalid blog data format.")
        st.json(blog_data)
        return
    
    blog = blog_data.get('blog', {})
    
    if isinstance(blog, dict):
        title = blog.get('title', 'Untitled')
        content = blog.get('content', 'No content generated')
    else:
        # Handle Pydantic model case
        title = getattr(blog, 'title', 'Untitled')
        content = getattr(blog, 'content', 'No content generated')
    
    # Display title
    st.markdown(f"### {title}")
    
    # Display content with markdown rendering
    st.markdown('<div class="blog-content">', unsafe_allow_html=True)
    st.markdown(content)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get topic for filename
    topic = st.session_state.get('blog_metadata', {}).get('topic', 'blog')
    
    # Download button
    ui_config = get_config()
    blog_text = f"# {title}\n\n{content}"
    st.download_button(
        label=ui_config.get_ui_text('DOWNLOAD_BUTTON_TEXT', '📥 Download Blog as Markdown'),
        data=blog_text,
        file_name=f"blog_{topic.replace(' ', '_')}.md",
        mime="text/markdown"
    )
    
    # Clear button
    if st.button(ui_config.get_ui_text('CLEAR_BUTTON_TEXT', '🗑️ Clear and Generate New'), use_container_width=True):
        if 'blog_data' in st.session_state:
            del st.session_state['blog_data']
        if 'blog_metadata' in st.session_state:
            del st.session_state['blog_metadata']
        st.rerun()

