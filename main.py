#!/usr/bin/env python3
"""
The-Gist: Book Summary to Audio Generator

A powerful CLI tool that uses an agentic AI workflow to:
1. Research popular books
2. Generate engaging summaries
3. Convert summaries to professional audio

Usage:
    python main.py summarize "Atomic Habits"
    python main.py summarize "Deep Work" --author "Cal Newport" --style executive
    python main.py batch books.json --length long
"""

import asyncio
import json
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from config import get_settings, SUMMARY_STYLES, SUMMARY_LENGTHS
from agents import OrchestratorAgent

# Initialize CLI app
app = typer.Typer(
    name="the-gist",
    help="📖 The Gist - Transform popular books into audio summaries",
    add_completion=False,
)
console = Console()


def get_banner():
    """Return the ASCII banner."""
    return """
╔════════════════════════════════════════════════════════════╗
║  _____ _            ____  _     _                          ║
║ |_   _| |__   ___  / ___|| |__ (_)___| |_                  ║
║   | | | '_ \ / _ \| |  _ | '_ \| / __| __|                 ║
║   | | | | | |  __/| |_| || | | | \__ \ |_                  ║
║   |_| |_| |_|\___| \____||_| |_|_|___/\__|                 ║
║                                                            ║
║   Core Wisdom, Instantly.                                  ║
╚════════════════════════════════════════════════════════════╝
"""


@app.command()
def summarize(
    book_title: str = typer.Argument(..., help="Title of the book to summarize"),
    author: Optional[str] = typer.Option(None, "--author", "-a", help="Author name for disambiguation"),
    style: str = typer.Option(
        "engaging",
        "--style", "-s",
        help="Summary style: engaging, academic, conversational, executive"
    ),
    length: str = typer.Option(
        "medium",
        "--length", "-l",
        help="Summary length: short (2-3min), medium (5-7min), long (10-15min), extended (20-25min)"
    ),
    voice: Optional[str] = typer.Option(
        None,
        "--voice", "-v",
        help="TTS voice: alloy, echo, fable, onyx, nova, shimmer"
    ),
    output_dir: Path = typer.Option(
        Path("output"),
        "--output", "-o",
        help="Output directory for audio files"
    ),
    audio_format: str = typer.Option(
        "mp3",
        "--format", "-f",
        help="Audio format: mp3, opus, aac, flac"
    ),
    text_only: bool = typer.Option(
        False,
        "--text-only", "-t",
        help="Generate summary text only, skip audio generation"
    ),
    save_summary: bool = typer.Option(
        True,
        "--save-summary",
        help="Save the text summary to a file"
    ),
):
    """
    Generate an audio summary for a book.
    
    Examples:
        python main.py summarize "Atomic Habits"
        python main.py summarize "Deep Work" --author "Cal Newport" --style executive
        python main.py summarize "Thinking, Fast and Slow" --length long --voice nova
    """
    console.print(get_banner(), style="bold cyan")
    
    # Validate inputs
    if style not in SUMMARY_STYLES:
        console.print(f"[red]Invalid style. Choose from: {', '.join(SUMMARY_STYLES.keys())}[/red]")
        raise typer.Exit(1)
    
    if length not in SUMMARY_LENGTHS:
        console.print(f"[red]Invalid length. Choose from: {', '.join(SUMMARY_LENGTHS.keys())}[/red]")
        raise typer.Exit(1)
    
    # Get settings
    settings = get_settings()
    
    if not settings.openai_api_key:
        console.print(Panel(
            "[red]OpenAI API key not found![/red]\n\n"
            "Please set your API key:\n"
            "  1. Create a .env file with: OPENAI_API_KEY=your-key-here\n"
            "  2. Or export: export OPENAI_API_KEY=your-key-here",
            title="⚠️ Configuration Error"
        ))
        raise typer.Exit(1)
    
    # Initialize orchestrator
    orchestrator = OrchestratorAgent(
        api_key=settings.openai_api_key,
        llm_model=settings.openai_model,
        tts_model=settings.tts_model,
        tts_voice=voice or settings.tts_voice,
        output_dir=output_dir,
        verbose=True
    )
    
    # Run the workflow
    result = asyncio.run(orchestrator.execute(
        book_title=book_title,
        author=author,
        style=style,
        length=length,
        voice=voice,
        audio_format=audio_format,
        skip_audio=text_only
    ))
    
    # Save summary text if requested
    if result.success and save_summary and result.summary_text:
        summary_path = output_dir / f"{_sanitize_filename(book_title)}_summary.txt"
        output_dir.mkdir(parents=True, exist_ok=True)
        summary_path.write_text(result.summary_text)
        console.print(f"[dim]Summary saved to: {summary_path}[/dim]")
    
    if not result.success:
        console.print(f"[red]Workflow failed: {result.error}[/red]")
        raise typer.Exit(1)
    
    console.print("\n[bold green]✨ Done! Enjoy your book summary.[/bold green]\n")


@app.command()
def batch(
    books_file: Path = typer.Argument(..., help="JSON file with list of books"),
    style: str = typer.Option("engaging", "--style", "-s"),
    length: str = typer.Option("medium", "--length", "-l"),
    output_dir: Path = typer.Option(Path("output"), "--output", "-o"),
    text_only: bool = typer.Option(False, "--text-only", "-t"),
):
    """
    Process multiple books from a JSON file.
    
    The JSON file should contain an array of book objects:
    [
        {"title": "Atomic Habits", "author": "James Clear"},
        {"title": "Deep Work", "author": "Cal Newport"}
    ]
    """
    console.print(get_banner(), style="bold cyan")
    
    if not books_file.exists():
        console.print(f"[red]File not found: {books_file}[/red]")
        raise typer.Exit(1)
    
    try:
        books = json.loads(books_file.read_text())
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON file: {e}[/red]")
        raise typer.Exit(1)
    
    settings = get_settings()
    
    if not settings.openai_api_key:
        console.print("[red]OpenAI API key not configured.[/red]")
        raise typer.Exit(1)
    
    orchestrator = OrchestratorAgent(
        api_key=settings.openai_api_key,
        llm_model=settings.openai_model,
        tts_model=settings.tts_model,
        tts_voice=settings.tts_voice,
        output_dir=output_dir,
        verbose=True
    )
    
    results = asyncio.run(orchestrator.process_batch(
        books=books,
        style=style,
        length=length,
        skip_audio=text_only
    ))
    
    # Summary
    successful = sum(1 for r in results if r.success)
    console.print(f"\n[bold]Batch complete: {successful}/{len(results)} books processed successfully[/bold]")


@app.command()
def list_voices():
    """Show available TTS voices with descriptions."""
    console.print("\n[bold]Available TTS Voices:[/bold]\n")
    
    voices = [
        ("alloy", "Neutral, balanced, clear", "General purpose"),
        ("echo", "Smooth, calm, documentary-style", "Biographies, history"),
        ("fable", "Expressive, dramatic, warm", "Fiction, storytelling"),
        ("onyx", "Deep, authoritative, confident", "Business, self-help"),
        ("nova", "Warm, friendly, conversational", "Casual, lifestyle"),
        ("shimmer", "Soft, gentle, soothing", "Meditation, wellness"),
    ]
    
    from rich.table import Table
    table = Table(show_header=True)
    table.add_column("Voice", style="cyan")
    table.add_column("Character")
    table.add_column("Best For")
    
    for voice, character, best_for in voices:
        table.add_row(voice, character, best_for)
    
    console.print(table)
    console.print("\n[dim]Use --voice <name> to select a voice[/dim]\n")


@app.command()
def list_styles():
    """Show available summary styles."""
    console.print("\n[bold]Available Summary Styles:[/bold]\n")
    
    from rich.table import Table
    table = Table(show_header=True)
    table.add_column("Style", style="cyan")
    table.add_column("Description")
    
    for style, description in SUMMARY_STYLES.items():
        table.add_row(style, description)
    
    console.print(table)
    console.print("\n[dim]Use --style <name> to select a style[/dim]\n")


@app.command()
def popular():
    """Show a list of popular books you can summarize."""
    console.print("\n[bold]📚 Popular Books to Summarize:[/bold]\n")
    
    from books_db import POPULAR_BOOKS
    from rich.table import Table
    
    table = Table(show_header=True)
    table.add_column("#", style="dim", width=3)
    table.add_column("Title", style="cyan")
    table.add_column("Author")
    table.add_column("Genre", style="dim")
    
    for i, book in enumerate(POPULAR_BOOKS[:20], 1):
        table.add_row(
            str(i),
            book["title"],
            book["author"],
            book.get("genre", "")
        )
    
    console.print(table)
    console.print("\n[dim]Try: python main.py summarize \"<title>\"[/dim]\n")


def _sanitize_filename(filename: str) -> str:
    """Create a safe filename."""
    invalid_chars = '<>:"/\\|?*'
    safe_name = filename
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '')
    return safe_name.replace(' ', '_').lower()[:50]


if __name__ == "__main__":
    app()

