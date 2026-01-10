"""
Configuration settings for The-Gist application.
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # OpenAI Configuration
    openai_api_key: str = Field(default="", env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-4o", env="OPENAI_MODEL")
    tts_model: str = Field(default="tts-1-hd", env="TTS_MODEL")
    tts_voice: str = Field(default="onyx", env="TTS_VOICE")
    
    # Available voices: alloy, echo, fable, onyx, nova, shimmer
    # onyx - deep, authoritative (great for non-fiction)
    # nova - warm, conversational
    # alloy - neutral, clear
    
    # Summary Configuration
    summary_style: str = Field(
        default="engaging",
        description="Style: engaging, academic, conversational, executive"
    )
    summary_length: str = Field(
        default="medium",
        description="Length: short (2-3 min), medium (5-7 min), long (10-15 min)"
    )
    
    # Output Configuration
    output_dir: Path = Field(default=Path("output"))
    audio_format: str = Field(default="mp3", env="AUDIO_FORMAT")
    
    # Agent Configuration
    max_retries: int = Field(default=3)
    verbose: bool = Field(default=True)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Summary length mappings (approximate word counts for audio duration)
SUMMARY_LENGTHS = {
    "short": {"words": 400, "description": "2-3 minute audio"},
    "medium": {"words": 900, "description": "5-7 minute audio"},
    "long": {"words": 1800, "description": "10-15 minute audio"},
    "extended": {"words": 3000, "description": "20-25 minute audio"},
}

# Summary styles with prompting guidance
SUMMARY_STYLES = {
    "engaging": "Write in an engaging, storytelling manner that captivates listeners",
    "academic": "Provide a scholarly analysis with key concepts and frameworks clearly explained",
    "conversational": "Write as if explaining the book to a friend over coffee",
    "executive": "Focus on actionable insights and key takeaways for busy professionals",
}

# Voice recommendations based on genre
VOICE_RECOMMENDATIONS = {
    "self-help": "onyx",      # Authoritative, motivational
    "business": "onyx",       # Professional, clear
    "fiction": "nova",        # Warm, storytelling
    "biography": "echo",      # Neutral, documentary style
    "science": "alloy",       # Clear, educational
    "philosophy": "fable",    # Thoughtful, measured
    "default": "onyx",
}


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()

