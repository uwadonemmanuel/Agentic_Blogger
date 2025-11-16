from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    
    def title_creation(self,state:BlogState):
        """
        create the title for the blog
        """

        if "topic" in state and state["topic"]:
            prompt="""
                   You are an expert blog content writer. Use Markdown formatting. Generate
                   a blog title for the {topic}. This title should be creative and SEO friendly

                   """
            
            sytem_message=prompt.format(topic=state["topic"])
            print(sytem_message)
            response=self.llm.invoke(sytem_message)
            print(response)
            return {"blog":{"title":response.content}}
        
    def content_generation(self,state:BlogState):
        if "topic" in state and state["topic"]:
            system_prompt = """You are expert blog writer. Use Markdown formatting.
            Generate a detailed blog content with detailed breakdown for the {topic}"""
            system_message = system_prompt.format(topic=state["topic"])
            response = self.llm.invoke(system_message)
            # Handle both dict and Pydantic model cases
            blog = state.get("blog", {})
            if isinstance(blog, dict):
                blog_title = blog.get("title", "")
            else:
                blog_title = getattr(blog, "title", "")
            return {"blog": {"title": blog_title, "content": response.content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        Supports: Hindi, French, Hausa, Yoruba, Igbo
        """
        language = state["current_language"].lower()
        
        # Language-specific instructions
        language_context = {
            "hindi": "Hindi (हिंदी)",
            "french": "French (Français)",
            "hausa": "Hausa (a West African language spoken primarily in Nigeria and Niger)",
            "yoruba": "Yoruba (a West African language spoken primarily in Nigeria and Benin)",
            "igbo": "Igbo (a West African language spoken primarily in Nigeria)"
        }
        
        language_name = language_context.get(language, language)
        
        translation_prompt="""
        Translate the following blog content into {language_name}.
        - Maintain the original tone, style, and formatting.
        - Adapt cultural references and idioms to be appropriate for {language_name}.
        - Keep the Markdown formatting intact.
        - Use proper grammar and natural phrasing in {language_name}.
        - Preserve technical terms when appropriate, but provide context if needed.

        ORIGINAL CONTENT:
        {blog_content}

        Return only the translated content, maintaining the same structure and formatting.
        """.format(language_name=language_name, blog_content="{blog_content}")
        print(state["current_language"])
        # Handle both dict and Pydantic model cases
        blog = state["blog"]
        if isinstance(blog, dict):
            blog_content = blog["content"]
            blog_title = blog.get("title", "")
        else:
            blog_content = blog.content
            blog_title = getattr(blog, "title", "")
        
        messages=[
            HumanMessage(translation_prompt.format(blog_content=blog_content))

        ]
        response = self.llm.invoke(messages)
        translated_content = response.content
        
        # Preserve the title and update content with translation
        return {"blog": {"title": blog_title, "content": translated_content}}

    def route(self, state: BlogState):
        return {"current_language": state['current_language'] }
    

    def route_decision(self, state: BlogState):
        """
        Route the content to the respective translation function.
        Supports: hindi, french, hausa, yoruba, igbo
        """
        language = state["current_language"].lower()
        
        # Supported languages mapping
        supported_languages = {
            "hindi": "hindi",
            "french": "french",
            "hausa": "hausa",
            "yoruba": "yoruba",
            "igbo": "igbo"
        }
        
        return supported_languages.get(language, language)