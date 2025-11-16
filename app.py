import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from src.graphs.graph_builder import GraphBuilder
from src.llms.llm_factory import LLMFactory, LLMModel

import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Agentic Blog Generator API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print(os.getenv("LANGCHAIN_API_KEY"))

os.environ["LANGSMITH_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

## API's

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Agentic Blog Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/blogs": "POST - Generate blog posts",
            "/models": "GET - List available models"
        }
    }

@app.get("/models")
async def get_models():
    """Get list of available LLM models"""
    from src.llms.llm_factory import MODEL_DISPLAY_NAMES, LLMModel
    
    models = []
    for model_enum in LLMModel:
        models.append({
            "id": model_enum.value,
            "name": MODEL_DISPLAY_NAMES.get(model_enum, model_enum.value),
            "provider": "openai"
        })
    
    return {"models": models}

@app.post("/blogs")
async def create_blogs(request: Request):
    """
    Generate a blog post
    
    Request body:
    - topic: str (required) - Blog topic
    - language: str (optional) - Translation language ('hindi', 'french', 'hausa', 'yoruba', or 'igbo')
    - model: str (optional) - OpenAI model to use (default: gpt-4o)
    - provider: str (optional) - LLM provider (only 'openai' is supported)
    - temperature: float (optional) - Generation temperature (default: 0.7)
    """
    data = await request.json()
    topic = data.get("topic", "")
    language = data.get("language", '')
    model = data.get("model", LLMModel.OPENAI_GPT_4O.value)
    provider = data.get("provider", "openai")  # Default to OpenAI
    temperature = data.get("temperature", 0.7)
    
    print(f"Generating blog with model: {model}, provider: {provider}, language: {language}")

    # Get the LLM object (OpenAI only)
    try:
        llm = LLMFactory.get_llm(
            model=model,
            provider=provider,
            temperature=temperature
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error": f"Failed to initialize LLM: {str(e)}",
                "message": "Please check your OPENAI_API_KEY in .env file",
                "model_used": model
            }
        )

    # Get the graph
    graph_builder = GraphBuilder(llm)
    
    try:
        if topic and language:
            graph = graph_builder.setup_graph(usecase="language")
            state = graph.invoke({"topic": topic, "current_language": language.lower()})
        elif topic:
            graph = graph_builder.setup_graph(usecase="topic")
            state = graph.invoke({"topic": topic})
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Topic is required",
                    "model_used": model
                }
            )
        
        return {
            "data": state,
            "model_used": model,
            "provider": "openai"
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": f"Failed to generate blog: {str(e)}",
                "model_used": model
            }
        )

if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)

