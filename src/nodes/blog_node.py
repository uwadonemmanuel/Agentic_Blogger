from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage, HumanMessage
from src.states.blogstate import Blog
import re

class BlogNode:
    """
    A class to represent he blog node
    """

    def __init__(self,llm):
        self.llm=llm

    def _remove_tldr(self, content: str) -> str:
        """
        Remove TL;DR sections from blog content.
        Handles various formats: TL;DR, TLDR, tl;dr, etc.
        """
        if not content:
            return content
        
        # Pattern to match TL;DR sections (case-insensitive)
        # Matches: "TL;DR:", "TLDR:", "tl;dr:", etc. followed by content until end or next major section
        patterns = [
            r'(?i)(?:^|\n)\s*(?:TL;DR|TLDR|tl;dr|tl;dr:)\s*:?\s*\n.*',  # TL;DR at start of line
            r'(?i)\n\s*(?:TL;DR|TLDR|tl;dr|tl;dr:)\s*:?\s*\n.*',  # TL;DR after newline
            r'(?i)(?:^|\n)\s*##?\s*(?:TL;DR|TLDR|tl;dr)\s*.*?(?=\n##|\Z)',  # TL;DR as heading
        ]
        
        cleaned_content = content
        for pattern in patterns:
            cleaned_content = re.sub(pattern, '', cleaned_content, flags=re.DOTALL | re.MULTILINE)
        
        # Also remove any standalone "TL;DR" lines
        lines = cleaned_content.split('\n')
        filtered_lines = []
        skip_next = False
        for i, line in enumerate(lines):
            # Skip lines that are just TL;DR variations
            if re.match(r'^\s*(?:TL;DR|TLDR|tl;dr|tl;dr:)\s*:?\s*$', line, re.IGNORECASE):
                skip_next = True
                continue
            # Skip the line immediately after TL;DR if it looks like a summary start
            if skip_next and (line.strip().startswith('-') or line.strip().startswith('*') or len(line.strip()) < 50):
                skip_next = False
                continue
            skip_next = False
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines).strip()
    
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
        """
        Generate blog content. If title exists, use it; otherwise generate title and content together.
        """
        if "topic" in state and state["topic"]:
            # Check if title already exists
            blog = state.get("blog", {})
            if isinstance(blog, dict):
                existing_title = blog.get("title", "")
            else:
                existing_title = getattr(blog, "title", "") if blog else ""
            
            if existing_title:
                # Title already exists, just generate content
                system_prompt = """You are an expert blog writer. Use Markdown formatting.
                Generate detailed blog content for the topic: {topic}
                The blog title is: {title}
                
                IMPORTANT: 
                - Do NOT include a TL;DR (Too Long; Didn't Read) section or summary at the end.
                - Write comprehensive, well-structured content (approximately 800-1200 words).
                - Use proper Markdown formatting with headers, lists, and paragraphs."""
                system_message = system_prompt.format(topic=state["topic"], title=existing_title)
            else:
                # Generate both title and content in one call for better performance
                system_prompt = """You are an expert blog writer. Use Markdown formatting.
                Generate a complete blog post for the topic: {topic}
                
                Format your response as follows:
                TITLE: [Your creative, SEO-friendly blog title here]
                
                CONTENT:
                [Your detailed blog content here]
                
                IMPORTANT: 
                - Do NOT include a TL;DR (Too Long; Didn't Read) section or summary at the end.
                - Write comprehensive, well-structured content (approximately 800-1200 words).
                - Use proper Markdown formatting with headers, lists, and paragraphs.
                - Start the content immediately after "CONTENT:" line."""
                system_message = system_prompt.format(topic=state["topic"])
            
            response = self.llm.invoke(system_message)
            content = response.content
            
            # If we generated both title and content, parse them
            if not existing_title and "TITLE:" in content and "CONTENT:" in content:
                parts = content.split("CONTENT:", 1)
                if len(parts) == 2:
                    title_part = parts[0].replace("TITLE:", "").strip()
                    content = parts[1].strip()
                    existing_title = title_part
            
            # Remove any TL;DR sections that might have been generated
            cleaned_content = self._remove_tldr(content)
            
            return {"blog": {"title": existing_title or "Untitled", "content": cleaned_content}}
        
    def translation(self,state:BlogState):
        """
        Translate the content to the specified language.
        Supports: Hindi, French, Hausa, Yoruba, Igbo
        Optimized for faster translation with concise prompts.
        """
        language = state["current_language"].lower()
        
        # Language-specific instructions (simplified for faster processing)
        language_context = {
            "hindi": "Hindi (हिंदी)",
            "french": "French (Français)",
            "hausa": "Hausa",
            "yoruba": "Yoruba",
            "igbo": "Igbo"
        }
        
        language_name = language_context.get(language, language)
        
        # Handle both dict and Pydantic model cases
        blog = state["blog"]
        if isinstance(blog, dict):
            blog_content = blog["content"]
            blog_title = blog.get("title", "")
        else:
            blog_content = blog.content
            blog_title = getattr(blog, "title", "")
        
        # Optimized, concise translation prompt for faster processing
        translation_prompt = """Translate this blog to {language_name}. Keep Markdown formatting and structure. Return only the translated content.

{blog_content}""".format(language_name=language_name, blog_content=blog_content)
        
        print(f"Translating to {state['current_language']}...")
        
        try:
            messages = [HumanMessage(translation_prompt)]
            # For translation, create a temporary LLM with higher max_tokens
            # Translation needs more tokens since we're translating existing content
            from src.llms.llm_factory import LLMFactory
            import os
            
            # Get model name and temperature from current LLM
            model_name = getattr(self.llm, 'model_name', None) or getattr(self.llm, 'model', 'gpt-4o')
            temperature = getattr(self.llm, 'temperature', 0.7)
            
            # Create translation LLM with higher max_tokens and timeout
            translation_llm = LLMFactory.get_llm(
                model=model_name,
                temperature=temperature,
                max_tokens=6000,  # Higher limit for translations
                timeout=300  # 5 minute timeout
            )
            
            response = translation_llm.invoke(messages)
            translated_content = response.content
            
            # Remove any TL;DR sections from translated content
            cleaned_translated_content = self._remove_tldr(translated_content)
            
            # Preserve the title and update content with translation
            return {"blog": {"title": blog_title, "content": cleaned_translated_content}}
        except Exception as e:
            print(f"Translation error: {str(e)}")
            # Return original content if translation fails
            return {"blog": {"title": blog_title, "content": blog_content}}

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