# Agentic Blog Generator

An AI-powered Agentic blog generation application built with LangGraph, FastAPI, and Streamlit. This app uses OpenAI models to generate blog posts on any topic and can translate them to Hindi, French, Hausa, Yoruba, or Igbo.

## Features

- 📝 **Topic-based Blog Generation**: Generate comprehensive blog posts on any topic
- 🌍 **Multi-language Support**: Translate blogs to Hindi, French, Hausa, Yoruba, or Igbo
- 🤖 **OpenAI Models**: Support for latest GPT models (as of November 2025)
  - **GPT-5 Series**: GPT-5, GPT-5 Mini (Latest Generation, released August 2025)
  - **GPT-4.1 Series**: GPT-4.1, GPT-4.1 Mini, GPT-4.1 Nano (Enhanced coding & long context, released April 2025)
  - **GPT-4o Series**: GPT-4o, GPT-4o Mini (Reinstated for paid subscribers)
  - **GPT-3.5 Series**: GPT-3.5 Turbo (Fast & cost-effective)
- 🎨 **Modular Streamlit UI**: Beautiful, modular web interface with LLM selection
  - **Component-based architecture**: Separated into sidebar, main content, styles
  - **Configuration-driven**: Customize via `uiconfigfile.ini`
  - **Easy to extend**: Add new UI components without modifying core logic
- 🔍 **LangGraph Studio**: Visualize and debug your graphs/agents
- 🔄 **FastAPI Backend**: RESTful API for programmatic access
- ⚙️ **Customizable Settings**: Adjust temperature and model selection via config file

## Project Structure

```
AgenticBlogger/
├── app.py                    # FastAPI backend server
├── streamlit_app.py          # Streamlit app entry point (simple runner)
├── graph.png                 # Langraph image generated
├── src/
│   ├── graphs/              # LangGraph definitions
│   │   └── graph_builder.py # Graph construction and compilation
│   ├── nodes/               # Graph nodes (blog generation logic)
│   │   └── blog_node.py     # Blog generation, translation, routing nodes
│   ├── states/              # State definitions
│   │   └── blogstate.py     # BlogState and Blog Pydantic models
│   ├── llms/                # LLM configuration
│   │   └── llm_factory.py   # OpenAI LLM factory (single provider)
│   └── ui/                   # Modular Streamlit UI components
│       ├── __init__.py       # UI module exports
│       ├── blog_generator_ui.py  # Main UI orchestrator
│       ├── sidebar.py        # Sidebar configuration component
│       ├── main_content.py   # Main content and blog output
│       ├── styles.py         # CSS styles, header, footer
│       ├── config_loader.py   # Configuration file loader
│       └── uiconfigfile.ini  # UI configuration file
├── langgraph.json           # LangGraph Studio configuration
├── requirements.txt         # Python dependencies
└── pyproject.toml           # Project metadata
```

## Setup

### 1. Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using uv
uv pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the root directory:

```env
# Required for OpenAI models
OPENAI_API_KEY=your_openai_api_key_here

# Required for LangGraph Studio
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

**Note**: You need `OPENAI_API_KEY` to use the app. Get your API key from https://platform.openai.com/api-keys

### 3. Run the Application

#### Option A: Streamlit UI (Recommended)

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

#### Option B: FastAPI Backend Only

```bash
python app.py
```

The API will be available at `http://localhost:8000`

#### Option C: Both (FastAPI + Streamlit)

Terminal 1 (FastAPI):
```bash
python app.py
```

Terminal 2 (Streamlit):
```bash
streamlit run streamlit_app.py
```

## Usage

### Streamlit Interface

1. Open the Streamlit app in your browser
2. In the sidebar, select an OpenAI model (default: GPT-4o)
3. Adjust temperature if needed (controls creativity)
4. Enter a blog topic (e.g., "Artificial Intelligence")
5. Optionally select a translation language:
   - Hindi (हिंदी)
   - French (Français)
   - Hausa (Nigerian language)
   - Yoruba (Nigerian language)
   - Igbo (Nigerian language)
6. Click "Generate Blog"
7. View and download your generated blog

### FastAPI Endpoint

```bash
# Generate blog with topic only (uses default model: gpt-4o)
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Python Programming"}'

# Generate blog with translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Machine Learning", "language": "french"}'

# Generate blog with specific OpenAI model
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "AI Agents",
    "language": "hindi",
    "model": "gpt-4o",
    "temperature": 0.8
  }'

# Generate blog with GPT-5 (latest) in Yoruba
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Future of AI",
    "language": "yoruba",
    "model": "gpt-5",
    "temperature": 0.7
  }'

# Generate blog in Hausa
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Technology in Africa",
    "language": "hausa",
    "model": "gpt-4o"
  }'

# Generate blog in Igbo
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Cultural Heritage",
    "language": "igbo",
    "model": "gpt-4o"
  }'

# List available models
curl http://localhost:8000/models
```

## LangGraph Studio

LangGraph Studio allows you to visualize and debug your graphs/agents.

### Setup

1. Make sure you have `langgraph-cli[inmem]` installed (included in requirements.txt)
2. Ensure your `.env` file has `LANGCHAIN_API_KEY` set

### Running Studio

```bash
langgraph dev
```

This will:
- Start the LangGraph Studio server
- Open the Studio UI in your browser
- Allow you to visualize the graph structure
- Enable debugging and step-through execution
- Show state transitions in real-time

### Graph Configuration

The graph is configured in `langgraph.json`:

```json
{
    "dependencies": ["."],
    "graphs": {
        "blog_generator_agent": "./src/graphs/graph_builder.py:graph"
    },
    "env": "./.env"
}
```

The graph is exported from `src/graphs/graph_builder.py` as the `graph` variable.

## UI Configuration

The Streamlit UI is modular and configuration-driven. Customize the app by editing `src/ui/uiconfigfile.ini`:

### Configuration File

The `uiconfigfile.ini` file allows you to customize:

- **Page Settings**: Title, icon, layout
- **API Configuration**: Endpoint URL, timeout
- **LLM Defaults**: Default model, temperature range
- **Supported Languages**: Add or remove languages
- **UI Text**: All button labels, headers, and messages
- **About Section**: Feature descriptions

### Example Configuration

```ini
[DEFAULT]
PAGE_TITLE = Agentic Blog Generator
DEFAULT_MODEL = gpt-4o
API_ENDPOINT = http://localhost:8000/blogs
LANGUAGES = hindi, french, hausa, yoruba, igbo
```

### UI Architecture

The UI is split into modular components:

- **`blog_generator_ui.py`**: Main orchestrator that coordinates all components
- **`sidebar.py`**: Handles configuration, LLM selection, and about section
- **`main_content.py`**: Blog input form, generation handling, and output display
- **`styles.py`**: CSS styling, header, and footer
- **`config_loader.py`**: Reads and parses `uiconfigfile.ini`

### Customizing the UI

1. **Change UI Text**: Edit `src/ui/uiconfigfile.ini`
2. **Modify Components**: Edit individual component files in `src/ui/`
3. **Add New Features**: Create new components and import in `blog_generator_ui.py`


## Development

### Graph Structure

The application uses two graph types:

1. **Topic Graph**: Simple blog generation (title → content)
2. **Language Graph**: Blog generation with translation (title → content → route → translation)

### Adding New Features

1. **New Node**: Add to `src/nodes/blog_node.py`
2. **New State Field**: Update `src/states/blogstate.py`
3. **Graph Modification**: Edit `src/graphs/graph_builder.py`
4. **New UI Component**: Create in `src/ui/` and import in `blog_generator_ui.py`
5. **New Language**: Add to `src/nodes/blog_node.py` route_decision and `src/graphs/graph_builder.py`
6. **UI Configuration**: Update `src/ui/uiconfigfile.ini`

### Testing

Test the FastAPI endpoint:

```bash
# Test topic-only generation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic"}'

# Test with Hindi translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "language": "hindi"}'

# Test with French translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "language": "french"}'

# Test with Hausa translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "language": "hausa"}'

# Test with Yoruba translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "language": "yoruba"}'

# Test with Igbo translation
curl -X POST "http://localhost:8000/blogs" \
  -H "Content-Type: application/json" \
  -d '{"topic": "Test Topic", "language": "igbo"}'
```

## Troubleshooting

### SSL/Network Errors During Installation

If you encounter SSL errors when installing packages:

```bash
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org <package>
```

### LLM API Errors

**OpenAI:**
- Ensure `OPENAI_API_KEY` is set in `.env`
- Check your API key is valid and has credits
- Verify you have access to the selected model (some models like GPT-5 may require special access)
- Check your OpenAI account billing status
- Use the `/models` endpoint to see available models
- Check model names match exactly (case-sensitive)

### LangGraph Studio Not Starting

- Verify `LANGCHAIN_API_KEY` is set
- Check that `langgraph-cli[inmem]` is installed
- Ensure the graph is properly exported in `graph_builder.py`

### Streamlit Connection Errors

- Make sure FastAPI is running on port 8000
- Check the API endpoint URL in Streamlit sidebar
- Verify CORS settings if accessing from different origin

## API Reference

### POST /blogs

Generate a blog post.

**Request Body:**
```json
{
  "topic": "string (required)",
  "language": "string (optional: 'hindi', 'french', 'hausa', 'yoruba', or 'igbo')",
  "model": "string (optional: OpenAI model name, default: 'gpt-4o')",
  "provider": "string (optional: only 'openai' is supported)",
  "temperature": "float (optional: 0.0-2.0, default: 0.7)"
}
```

**Response:**
```json
{
  "data": {
    "topic": "string",
    "blog": {
      "title": "string",
      "content": "string"
    },
    "current_language": "string"
  },
  "model_used": "string",
  "provider": "string"
}
```

## License

This project is part of the Andela GenAI program.

## Support

For issues or questions, please check:
- LangGraph Documentation: https://langchain-ai.github.io/langgraph/
- OpenAI API Documentation: https://platform.openai.com/docs
- Streamlit Documentation: https://docs.streamlit.io/

