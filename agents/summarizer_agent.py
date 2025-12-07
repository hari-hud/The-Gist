"""
Summarizer Agent - Generates engaging book summaries.
"""
import time
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from .base_agent import BaseAgent, AgentResult
from config import SUMMARY_LENGTHS, SUMMARY_STYLES


class SummarizerAgent(BaseAgent):
    """
    Agent responsible for generating compelling book summaries.
    Creates audio-optimized content with proper pacing and structure.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4o", verbose: bool = True):
        super().__init__(name="SummarizerAgent", verbose=verbose)
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        
    async def execute(
        self,
        research_data: Dict[str, Any],
        style: str = "engaging",
        length: str = "medium",
        **kwargs
    ) -> AgentResult:
        """
        Generate a book summary optimized for audio narration.
        
        Args:
            research_data: Book research from ResearchAgent
            style: Summary style (engaging, academic, conversational, executive)
            length: Summary length (short, medium, long, extended)
            
        Returns:
            AgentResult with generated summary
        """
        start_time = time.time()
        
        title = research_data.get("title", "Unknown Book")
        self.log_thinking(f"Crafting {length} {style} summary for '{title}'...")
        
        try:
            # Get configuration
            length_config = SUMMARY_LENGTHS.get(length, SUMMARY_LENGTHS["medium"])
            style_guidance = SUMMARY_STYLES.get(style, SUMMARY_STYLES["engaging"])
            target_words = length_config["words"]
            
            prompt = self._build_summary_prompt(research_data, style_guidance, target_words)
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000
            )
            
            summary = response.choices[0].message.content
            word_count = len(summary.split())
            
            execution_time = time.time() - start_time
            self.log_success(f"Summary generated: {word_count} words (~{word_count // 150} min audio)")
            
            return AgentResult(
                success=True,
                data={
                    "summary": summary,
                    "word_count": word_count,
                    "estimated_audio_duration": f"{word_count // 150}-{word_count // 130} minutes",
                    "style": style,
                    "length": length
                },
                agent_name=self.name,
                execution_time=execution_time,
                metadata={
                    "model": self.model,
                    "tokens_used": response.usage.total_tokens if response.usage else 0,
                    "target_words": target_words
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_error(f"Summary generation failed: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                agent_name=self.name,
                execution_time=execution_time,
                error=str(e)
            )
    
    def _get_system_prompt(self) -> str:
        """System prompt for the summarizer."""
        return """You are an expert book summarizer who creates compelling audio content. 
Your summaries are:
- Optimized for audio listening (clear transitions, good pacing)
- Engaging from the first sentence with a hook
- Structured with clear sections that flow naturally
- Rich with key insights, examples, and actionable takeaways
- Written to be spoken aloud (avoiding complex punctuation, parentheticals)

You capture the essence and transformative ideas of books while making them accessible and memorable.
Write in a way that sounds natural when read aloud - use conversational connectors, rhetorical questions, and varied sentence lengths."""

    def _build_summary_prompt(
        self, 
        research_data: Dict[str, Any], 
        style_guidance: str,
        target_words: int
    ) -> str:
        """Build the summary generation prompt."""
        
        title = research_data.get("title", "Unknown")
        author = research_data.get("author", "Unknown")
        genre = research_data.get("genre", "")
        themes = ", ".join(research_data.get("main_themes", []))
        concepts = ", ".join(research_data.get("key_concepts", []))
        core_message = research_data.get("core_message", "")
        why_popular = research_data.get("why_popular", "")
        audience = research_data.get("target_audience", "")
        
        return f"""Create a compelling audio summary of "{title}" by {author}.

**Book Context:**
- Genre: {genre}
- Main Themes: {themes}
- Key Concepts: {concepts}
- Core Message: {core_message}
- Why It's Popular: {why_popular}
- Target Audience: {audience}

**Your Task:**
{style_guidance}

**Structure your summary as follows:**
1. **Opening Hook** (grab attention, why this book matters)
2. **Author Context** (brief, relevant background)
3. **Core Ideas** (the main insights, explained clearly with examples)
4. **Key Takeaways** (3-5 actionable insights listeners can apply)
5. **Closing Thought** (memorable ending, call to reflection or action)

**Audio Optimization Guidelines:**
- Use clear section transitions ("Now, let's explore...", "Here's where it gets interesting...")
- Vary sentence length for natural rhythm
- Include brief pauses with phrases like "Think about that for a moment."
- Avoid parenthetical asides and complex punctuation
- Use rhetorical questions to engage listeners
- Include specific examples and stories from the book

**Target Length:** Approximately {target_words} words ({target_words // 150}-{target_words // 130} minutes when spoken)

Write the complete summary now:"""

