"""
Research Agent - Gathers book information and context.
"""
import time
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from .base_agent import BaseAgent, AgentResult


class ResearchAgent(BaseAgent):
    """
    Agent responsible for researching book information.
    Gathers context about the book, author, themes, and target audience.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o", verbose: bool = True):
        super().__init__(name="ResearchAgent", verbose=verbose)
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        
    async def execute(
        self,
        book_title: str,
        author: Optional[str] = None,
        **kwargs
    ) -> AgentResult:
        """
        Research a book and gather comprehensive information.
        
        Args:
            book_title: Title of the book to research
            author: Optional author name for disambiguation
            
        Returns:
            AgentResult with book research data
        """
        start_time = time.time()
        self.log_thinking(f"Researching '{book_title}'...")
        
        try:
            author_context = f" by {author}" if author else ""
            
            prompt = f"""You are a literary research assistant. Research the book "{book_title}"{author_context}.

Provide comprehensive information in the following JSON structure:
{{
    "title": "Full book title",
    "author": "Author name",
    "publication_year": "Year published",
    "genre": "Primary genre (e.g., self-help, business, fiction, biography, science, philosophy)",
    "subgenres": ["list", "of", "subgenres"],
    "target_audience": "Description of who this book is for",
    "main_themes": ["theme1", "theme2", "theme3"],
    "key_concepts": ["concept1", "concept2", "concept3"],
    "why_popular": "Brief explanation of why this book became popular/impactful",
    "author_background": "Brief author bio relevant to the book",
    "book_structure": "How the book is organized (chapters, parts, etc.)",
    "notable_quotes_topics": ["Topics of famous quotes from the book"],
    "similar_books": ["Similar book 1", "Similar book 2"],
    "estimated_reading_time": "Hours for average reader",
    "core_message": "The single most important message of the book in one sentence"
}}

Return ONLY the JSON, no additional text."""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert literary researcher with encyclopedic knowledge of popular books. Respond only with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            import json
            research_data = json.loads(response.choices[0].message.content)
            
            execution_time = time.time() - start_time
            self.log_success(f"Research complete for '{research_data.get('title', book_title)}'")
            
            return AgentResult(
                success=True,
                data=research_data,
                agent_name=self.name,
                execution_time=execution_time,
                metadata={
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens if response.usage else 0
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_error(f"Research failed: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                agent_name=self.name,
                execution_time=execution_time,
                error=str(e)
            )

