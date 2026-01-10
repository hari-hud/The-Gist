"""
Orchestrator Agent - Coordinates the complete book summary workflow.
"""
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime

from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
from rich.table import Table

from .base_agent import BaseAgent, AgentResult
from .research_agent import ResearchAgent
from .summarizer_agent import SummarizerAgent
from .narrator_agent import NarratorAgent


console = Console()


@dataclass
class WorkflowResult:
    """Complete result of the book-to-audio workflow."""
    success: bool
    book_title: str
    audio_path: Optional[str]
    summary_text: Optional[str]
    word_count: int
    total_time: float
    agent_results: Dict[str, AgentResult]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "success": self.success,
            "book_title": self.book_title,
            "audio_path": self.audio_path,
            "word_count": self.word_count,
            "total_time_seconds": round(self.total_time, 2),
            "timestamp": datetime.now().isoformat(),
            "error": self.error
        }


class OrchestratorAgent(BaseAgent):
    """
    Master agent that coordinates the entire book-to-audio workflow.
    
    Workflow Steps:
    1. Research: Gather book information and context
    2. Summarize: Generate an engaging, audio-optimized summary
    3. Narrate: Convert the summary to professional audio
    """
    
    def __init__(
        self,
        api_key: str,
        llm_model: str = "gpt-4o",
        tts_model: str = "tts-1-hd",
        tts_voice: str = "onyx",
        output_dir: Path = Path("output"),
        verbose: bool = True
    ):
        super().__init__(name="Orchestrator", verbose=verbose)
        
        self.api_key = api_key
        self.output_dir = Path(output_dir)
        
        # Initialize sub-agents
        self.research_agent = ResearchAgent(
            api_key=api_key,
            model=llm_model,
            verbose=verbose
        )
        self.summarizer_agent = SummarizerAgent(
            api_key=api_key,
            model=llm_model,
            verbose=verbose
        )
        self.narrator_agent = NarratorAgent(
            api_key=api_key,
            tts_model=tts_model,
            default_voice=tts_voice,
            verbose=verbose
        )
        
    async def execute(
        self,
        book_title: str,
        author: Optional[str] = None,
        style: str = "engaging",
        length: str = "medium",
        voice: Optional[str] = None,
        audio_format: str = "mp3",
        skip_audio: bool = False,
        **kwargs
    ) -> WorkflowResult:
        """
        Execute the complete book-to-audio workflow.
        
        Args:
            book_title: Title of the book to summarize
            author: Optional author name
            style: Summary style (engaging, academic, conversational, executive)
            length: Summary length (short, medium, long, extended)
            voice: Override TTS voice selection
            audio_format: Audio output format
            skip_audio: If True, only generate summary (no audio)
            
        Returns:
            WorkflowResult with complete workflow data
        """
        start_time = time.time()
        agent_results = {}
        
        self._show_workflow_header(book_title, style, length)
        
        try:
            # Step 1: Research
            self.log("📚 Step 1/3: Researching book...", style="bold cyan")
            research_result = await self.research_agent.execute(
                book_title=book_title,
                author=author
            )
            agent_results["research"] = research_result
            
            if not research_result.success:
                raise Exception(f"Research failed: {research_result.error}")
            
            research_data = research_result.data
            self._show_research_summary(research_data)
            
            # Step 2: Summarize
            self.log("✍️ Step 2/3: Generating summary...", style="bold cyan")
            summary_result = await self.summarizer_agent.execute(
                research_data=research_data,
                style=style,
                length=length
            )
            agent_results["summary"] = summary_result
            
            if not summary_result.success:
                raise Exception(f"Summary failed: {summary_result.error}")
            
            summary_data = summary_result.data
            
            # Step 3: Narrate (optional)
            audio_path = None
            if not skip_audio:
                self.log("🎙️ Step 3/3: Generating audio...", style="bold cyan")
                narrator_result = await self.narrator_agent.execute(
                    summary_data=summary_data,
                    book_title=book_title,
                    genre=research_data.get("genre"),
                    voice=voice,
                    output_dir=self.output_dir,
                    audio_format=audio_format
                )
                agent_results["narrator"] = narrator_result
                
                if not narrator_result.success:
                    raise Exception(f"Audio generation failed: {narrator_result.error}")
                
                audio_path = narrator_result.data.get("audio_path")
            else:
                self.log("⏭️ Step 3/3: Skipping audio generation", style="dim")
            
            total_time = time.time() - start_time
            
            # Show final results
            self._show_completion_summary(
                book_title=research_data.get("title", book_title),
                summary_data=summary_data,
                audio_path=audio_path,
                total_time=total_time
            )
            
            return WorkflowResult(
                success=True,
                book_title=research_data.get("title", book_title),
                audio_path=audio_path,
                summary_text=summary_data.get("summary"),
                word_count=summary_data.get("word_count", 0),
                total_time=total_time,
                agent_results=agent_results
            )
            
        except Exception as e:
            total_time = time.time() - start_time
            self.log_error(f"Workflow failed: {str(e)}")
            
            return WorkflowResult(
                success=False,
                book_title=book_title,
                audio_path=None,
                summary_text=None,
                word_count=0,
                total_time=total_time,
                agent_results=agent_results,
                error=str(e)
            )
    
    async def process_batch(
        self,
        books: List[Dict[str, Any]],
        **kwargs
    ) -> List[WorkflowResult]:
        """
        Process multiple books in sequence.
        
        Args:
            books: List of book dicts with 'title' and optional 'author'
            **kwargs: Additional arguments passed to execute()
            
        Returns:
            List of WorkflowResults
        """
        results = []
        total = len(books)
        
        console.print(f"\n[bold]Processing {total} books...[/bold]\n")
        
        for i, book in enumerate(books, 1):
            console.print(f"\n{'='*60}")
            console.print(f"[bold]Book {i}/{total}[/bold]")
            console.print(f"{'='*60}\n")
            
            result = await self.execute(
                book_title=book.get("title", ""),
                author=book.get("author"),
                **kwargs
            )
            results.append(result)
            
            # Brief pause between books to avoid rate limits
            if i < total:
                await asyncio.sleep(2)
        
        self._show_batch_summary(results)
        return results
    
    def _show_workflow_header(self, book_title: str, style: str, length: str):
        """Display workflow start header."""
        header = f"""
📖 [bold]The Gist[/bold] - Book Summary Generator

[cyan]Book:[/cyan] {book_title}
[cyan]Style:[/cyan] {style}
[cyan]Length:[/cyan] {length}
"""
        console.print(Panel(header, border_style="blue", title="🚀 Starting Workflow"))
    
    def _show_research_summary(self, data: Dict[str, Any]):
        """Display research findings."""
        table = Table(title="📚 Book Research", show_header=False, border_style="dim")
        table.add_column("Field", style="cyan")
        table.add_column("Value")
        
        table.add_row("Title", data.get("title", "N/A"))
        table.add_row("Author", data.get("author", "N/A"))
        table.add_row("Genre", data.get("genre", "N/A"))
        table.add_row("Themes", ", ".join(data.get("main_themes", [])[:3]))
        table.add_row("Core Message", data.get("core_message", "N/A")[:100] + "...")
        
        console.print(table)
        console.print()
    
    def _show_completion_summary(
        self,
        book_title: str,
        summary_data: Dict[str, Any],
        audio_path: Optional[str],
        total_time: float
    ):
        """Display workflow completion summary."""
        summary = f"""
✅ [bold green]Workflow Complete![/bold green]

[cyan]Book:[/cyan] {book_title}
[cyan]Summary:[/cyan] {summary_data.get('word_count', 0)} words
[cyan]Estimated Duration:[/cyan] {summary_data.get('estimated_audio_duration', 'N/A')}
[cyan]Audio File:[/cyan] {audio_path or 'Skipped'}
[cyan]Total Time:[/cyan] {total_time:.1f} seconds
"""
        console.print(Panel(summary, border_style="green", title="🎉 Complete"))
    
    def _show_batch_summary(self, results: List[WorkflowResult]):
        """Display batch processing summary."""
        successful = sum(1 for r in results if r.success)
        failed = len(results) - successful
        
        table = Table(title="📊 Batch Summary")
        table.add_column("Book", style="cyan")
        table.add_column("Status")
        table.add_column("Words", justify="right")
        table.add_column("Time", justify="right")
        
        for result in results:
            status = "✅" if result.success else "❌"
            table.add_row(
                result.book_title[:40],
                status,
                str(result.word_count),
                f"{result.total_time:.1f}s"
            )
        
        console.print(table)
        console.print(f"\n[bold]Results:[/bold] {successful} successful, {failed} failed")

