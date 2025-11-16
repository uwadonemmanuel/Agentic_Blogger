from langgraph.graph import StateGraph, START, END
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm

    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        graph = StateGraph(BlogState)
        blog_node_obj = BlogNode(self.llm)
        print(self.llm)
        ## Nodes
        graph.add_node("title_creation", blog_node_obj.title_creation)
        graph.add_node("content_generation", blog_node_obj.content_generation)

        ## Edges
        graph.add_edge(START,"title_creation")
        graph.add_edge("title_creation","content_generation")
        graph.add_edge("content_generation",END)

        return graph
    
    def build_language_graph(self):
        """
        Build a graph for blog generation with inputs topic and language
        Supports: Hindi, French, Hausa, Yoruba, Igbo
        """
        graph = StateGraph(BlogState)
        blog_node_obj = BlogNode(self.llm)
        print(self.llm)
        
        ## Nodes
        graph.add_node("title_creation", blog_node_obj.title_creation)
        graph.add_node("content_generation", blog_node_obj.content_generation)
        
        # Translation nodes for all supported languages
        graph.add_node("hindi_translation", lambda state: blog_node_obj.translation({**state, "current_language": "hindi"}))
        graph.add_node("french_translation", lambda state: blog_node_obj.translation({**state, "current_language": "french"}))
        graph.add_node("hausa_translation", lambda state: blog_node_obj.translation({**state, "current_language": "hausa"}))
        graph.add_node("yoruba_translation", lambda state: blog_node_obj.translation({**state, "current_language": "yoruba"}))
        graph.add_node("igbo_translation", lambda state: blog_node_obj.translation({**state, "current_language": "igbo"}))
        
        graph.add_node("route", blog_node_obj.route)

        ## edges and conditional edges
        graph.add_edge(START, "title_creation")
        graph.add_edge("title_creation", "content_generation")
        graph.add_edge("content_generation", "route")

        ## conditional edge - routes to appropriate translation node
        graph.add_conditional_edges(
            "route",
            blog_node_obj.route_decision,
            {
                "hindi": "hindi_translation",
                "french": "french_translation",
                "hausa": "hausa_translation",
                "yoruba": "yoruba_translation",
                "igbo": "igbo_translation"
            }
        )
        
        # All translation nodes lead to END
        graph.add_edge("hindi_translation", END)
        graph.add_edge("french_translation", END)
        graph.add_edge("hausa_translation", END)
        graph.add_edge("yoruba_translation", END)
        graph.add_edge("igbo_translation", END)
        
        return graph
    
    
    def setup_graph(self,usecase):
        if usecase=="topic":
            graph = self.build_topic_graph()
        elif usecase=="language":
            print("Language block")
            graph = self.build_language_graph()
        else:
            raise ValueError(f"Unknown usecase: {usecase}")

        return graph.compile()
    

## Below code is for the langsmith langgraph studio
# This graph is used by LangGraph Studio for visualization and debugging
from src.llms.llm_factory import LLMFactory, LLMModel

# Use default OpenAI model for Studio (can be changed)
llm = LLMFactory.get_llm(model=LLMModel.OPENAI_GPT_4O.value)
graph_builder = GraphBuilder(llm)
graph = graph_builder.build_language_graph().compile()

