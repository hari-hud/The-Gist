"""
Narrator Agent - Converts text summaries to professional audio.
"""
import time
import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from openai import AsyncOpenAI

from .base_agent import BaseAgent, AgentResult
from config import VOICE_RECOMMENDATIONS


class NarratorAgent(BaseAgent):
    """
    Agent responsible for converting text to speech.
    Produces high-quality, professionally-narrated audio files.
    """
    
    def __init__(
        self, 
        api_key: str, 
        tts_model: str = "tts-1-hd",
        default_voice: str = "onyx",
        verbose: bool = True
    ):
        super().__init__(name="NarratorAgent", verbose=verbose)
        self.client = AsyncOpenAI(api_key=api_key)
        self.tts_model = tts_model
        self.default_voice = default_voice
        
        # OpenAI TTS has a max of 4096 characters per request
        self.max_chunk_size = 4000
        
    async def execute(
        self,
        summary_data: Dict[str, Any],
        book_title: str,
        genre: Optional[str] = None,
        voice: Optional[str] = None,
        output_dir: Path = Path("output"),
        audio_format: str = "mp3",
        **kwargs
    ) -> AgentResult:
        """
        Convert a book summary to audio.
        
        Args:
            summary_data: Summary data from SummarizerAgent
            book_title: Title of the book (for filename)
            genre: Book genre (for voice selection)
            voice: Override voice selection
            output_dir: Directory to save audio files
            audio_format: Output format (mp3, opus, aac, flac)
            
        Returns:
            AgentResult with audio file path
        """
        start_time = time.time()
        
        text = summary_data.get("summary", "")
        if not text:
            return AgentResult(
                success=False,
                data=None,
                agent_name=self.name,
                error="No summary text provided"
            )
        
        # Select voice based on genre or use override
        selected_voice = voice or self._select_voice(genre)
        self.log_thinking(f"Narrating with voice '{selected_voice}' ({self.tts_model})...")
        
        try:
            # Ensure output directory exists
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate safe filename
            safe_title = self._sanitize_filename(book_title)
            output_path = output_dir / f"{safe_title}_summary.{audio_format}"
            
            # Split text into chunks if needed
            chunks = self._split_text(text)
            self.log(f"Processing {len(chunks)} audio segment(s)...")
            
            # Generate audio for each chunk
            audio_segments = []
            for i, chunk in enumerate(chunks, 1):
                self.log(f"  Generating segment {i}/{len(chunks)}...")
                audio_data = await self._generate_audio(chunk, selected_voice, audio_format)
                audio_segments.append(audio_data)
            
            # Combine segments if multiple
            if len(audio_segments) == 1:
                final_audio = audio_segments[0]
            else:
                final_audio = self._combine_audio_segments(audio_segments)
            
            # Write to file
            with open(output_path, "wb") as f:
                f.write(final_audio)
            
            file_size_mb = output_path.stat().st_size / (1024 * 1024)
            execution_time = time.time() - start_time
            
            self.log_success(f"Audio saved: {output_path} ({file_size_mb:.2f} MB)")
            
            return AgentResult(
                success=True,
                data={
                    "audio_path": str(output_path),
                    "file_size_mb": round(file_size_mb, 2),
                    "voice": selected_voice,
                    "format": audio_format,
                    "segments": len(chunks),
                    "estimated_duration": summary_data.get("estimated_audio_duration", "unknown")
                },
                agent_name=self.name,
                execution_time=execution_time,
                metadata={
                    "tts_model": self.tts_model,
                    "character_count": len(text)
                }
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.log_error(f"Audio generation failed: {str(e)}")
            return AgentResult(
                success=False,
                data=None,
                agent_name=self.name,
                execution_time=execution_time,
                error=str(e)
            )
    
    async def _generate_audio(
        self, 
        text: str, 
        voice: str, 
        audio_format: str
    ) -> bytes:
        """Generate audio for a text chunk."""
        response = await self.client.audio.speech.create(
            model=self.tts_model,
            voice=voice,
            input=text,
            response_format=audio_format
        )
        return response.content
    
    def _select_voice(self, genre: Optional[str]) -> str:
        """Select appropriate voice based on genre."""
        if genre:
            genre_lower = genre.lower()
            for key, voice in VOICE_RECOMMENDATIONS.items():
                if key in genre_lower:
                    return voice
        return self.default_voice
    
    def _split_text(self, text: str) -> list:
        """Split text into chunks respecting sentence boundaries."""
        if len(text) <= self.max_chunk_size:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences
        sentences = text.replace(".\n", ".|||").replace(". ", ".|||").split("|||")
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Add period back if it was removed
            if not sentence.endswith(('.', '!', '?')):
                sentence += '.'
            
            if len(current_chunk) + len(sentence) + 1 <= self.max_chunk_size:
                current_chunk += (" " if current_chunk else "") + sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def _combine_audio_segments(self, segments: list) -> bytes:
        """Combine multiple audio segments into one."""
        # For MP3, we can simply concatenate the bytes
        # For more complex formats, we'd need pydub
        return b"".join(segments)
    
    def _sanitize_filename(self, filename: str) -> str:
        """Create a safe filename from book title."""
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        safe_name = filename
        for char in invalid_chars:
            safe_name = safe_name.replace(char, '')
        
        # Replace spaces with underscores and limit length
        safe_name = safe_name.replace(' ', '_').lower()
        return safe_name[:50]  # Limit length

