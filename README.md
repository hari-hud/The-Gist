# 📖 The-Gist

**Core Wisdom, Instantly.** Get the key insights from best-selling books in concise, professionally-narrated audio summaries, powered by an efficient AI agentic workflow.

<p align="center">
  <img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-GPT--4o-green.svg" alt="OpenAI">
  <img src="https://img.shields.io/badge/TTS-HD%20Audio-orange.svg" alt="TTS">
</p>

## ✨ Features

- 🤖 **Agentic Workflow**: Multi-agent architecture with specialized agents for research, summarization, and narration
- 📚 **Smart Research**: Automatically gathers book context, themes, and key concepts
- ✍️ **Audio-Optimized Summaries**: Generates summaries specifically designed for listening
- 🎙️ **Professional Narration**: High-quality text-to-speech with multiple voice options
- 📊 **Batch Processing**: Summarize multiple books at once
- 🎨 **Beautiful CLI**: Rich, colorful terminal interface with progress tracking

## 🏗️ Architecture

The-Gist uses a multi-agent workflow pattern:

```
┌─────────────────────────────────────────────────────────────┐
│                    OrchestratorAgent                        │
│                 (Coordinates Workflow)                      │
└─────────────────────────────────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ ResearchAgent   │ │ SummarizerAgent │ │ NarratorAgent   │
│ ─────────────── │ │ ─────────────── │ │ ─────────────── │
│ • Book info     │ │ • Generate      │ │ • Text-to-      │
│ • Themes        │ │   engaging      │ │   Speech        │
│ • Key concepts  │ │   summaries     │ │ • Voice         │
│ • Context       │ │ • Audio-        │ │   selection     │
│                 │ │   optimized     │ │ • HD audio      │
└─────────────────┘ └─────────────────┘ └─────────────────┘
```

## 🚀 Quick Start

### 1. Installation

```bash
# Clone and navigate to the directory
cd The-Gist

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Generate Your First Summary

```bash
# Basic usage
python main.py summarize "Atomic Habits"

# With options
python main.py summarize "Deep Work" --author "Cal Newport" --style executive --length long

# Text only (no audio)
python main.py summarize "The Psychology of Money" --text-only
```

## 📖 Usage

### Single Book Summary

```bash
python main.py summarize "BOOK TITLE" [OPTIONS]
```

**Options:**
| Option | Description | Default |
|--------|-------------|---------|
| `--author`, `-a` | Author name (for disambiguation) | None |
| `--style`, `-s` | Summary style | `engaging` |
| `--length`, `-l` | Summary length | `medium` |
| `--voice`, `-v` | TTS voice | Auto-selected |
| `--output`, `-o` | Output directory | `output/` |
| `--format`, `-f` | Audio format | `mp3` |
| `--text-only`, `-t` | Skip audio generation | False |

### Batch Processing

Create a `books.json` file:

```json
[
    {"title": "Atomic Habits", "author": "James Clear"},
    {"title": "Deep Work", "author": "Cal Newport"},
    {"title": "The Psychology of Money", "author": "Morgan Housel"}
]
```

Run batch processing:

```bash
python main.py batch books.json --length medium --style engaging
```

### List Available Options

```bash
# Show available TTS voices
python main.py list-voices

# Show summary styles
python main.py list-styles

# Show popular books
python main.py popular
```

## 🎨 Summary Styles

| Style | Description |
|-------|-------------|
| `engaging` | Captivating, storytelling approach |
| `academic` | Scholarly analysis with frameworks |
| `conversational` | Like explaining to a friend |
| `executive` | Actionable insights for busy professionals |

## ⏱️ Summary Lengths

| Length | Duration | Word Count |
|--------|----------|------------|
| `short` | 2-3 min | ~400 words |
| `medium` | 5-7 min | ~900 words |
| `long` | 10-15 min | ~1800 words |
| `extended` | 20-25 min | ~3000 words |

## 🎙️ TTS Voices

| Voice | Character | Best For |
|-------|-----------|----------|
| `alloy` | Neutral, balanced | General purpose |
| `echo` | Smooth, calm | Biographies, history |
| `fable` | Expressive, dramatic | Fiction, storytelling |
| `onyx` | Deep, authoritative | Business, self-help |
| `nova` | Warm, friendly | Casual, lifestyle |
| `shimmer` | Soft, gentle | Meditation, wellness |

## 📁 Output

Generated files are saved to the `output/` directory:

```
output/
├── atomic_habits_summary.mp3      # Audio file
├── atomic_habits_summary.txt      # Text summary
├── deep_work_summary.mp3
└── deep_work_summary.txt
```

## 🔧 Advanced Configuration

### Environment Variables

```bash
# Models
OPENAI_MODEL=gpt-4o          # LLM model for summaries
TTS_MODEL=tts-1-hd           # TTS model (tts-1 or tts-1-hd)
TTS_VOICE=onyx               # Default voice

# Audio
AUDIO_FORMAT=mp3             # Output format
```

### Programmatic Usage

```python
import asyncio
from agents import OrchestratorAgent

async def generate_summary():
    orchestrator = OrchestratorAgent(
        api_key="your-api-key",
        llm_model="gpt-4o",
        tts_model="tts-1-hd"
    )
    
    result = await orchestrator.execute(
        book_title="Atomic Habits",
        author="James Clear",
        style="engaging",
        length="medium"
    )
    
    print(f"Audio saved to: {result.audio_path}")
    print(f"Word count: {result.word_count}")

asyncio.run(generate_summary())
```

## 📊 Example Output

```
╔════════════════════════════════════════════════════════════╗
║  The Gist - Book Summary Generator                         ║
╚════════════════════════════════════════════════════════════╝

🚀 Starting Workflow
   Book: Atomic Habits
   Style: engaging
   Length: medium

📚 Step 1/3: Researching book...
   🤖 [ResearchAgent] 💭 Researching 'Atomic Habits'...
   🤖 [ResearchAgent] ✅ Research complete

✍️ Step 2/3: Generating summary...
   🤖 [SummarizerAgent] 💭 Crafting medium engaging summary...
   🤖 [SummarizerAgent] ✅ Summary generated: 892 words (~6 min audio)

🎙️ Step 3/3: Generating audio...
   🤖 [NarratorAgent] 💭 Narrating with voice 'onyx'...
   🤖 [NarratorAgent] ✅ Audio saved: output/atomic_habits_summary.mp3

✅ Workflow Complete!
   Summary: 892 words
   Duration: ~6-7 minutes
   Audio: output/atomic_habits_summary.mp3
   Time: 45.2 seconds
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details.

---

<p align="center">
  Made with ❤️ for book lovers who are short on time
</p>
