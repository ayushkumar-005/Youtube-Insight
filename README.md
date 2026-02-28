# Youtube Insight

It is a Telegram YouTube Summarizer & Q&A Bot built with the OpenClaw framework, Python, and GLM-5. It acts as a personal AI research assistant, allowing users to extract structured insights from YouTube videos, ask contextual follow-up questions, and consume content in multiple languages (English and Other Indian Languages).

## 📋 Features

- **Instant Structured Summaries:** Automatically fetches transcripts and generates a strict format containing the video title, 5 key points, timestamps, and a core takeaway.
- **Autonomous Context Retrieval:** Handles massively long videos by truncating the initial payload to save tokens, then autonomously executing a local search script (`search_cache.py`) to find specific answers to deep-dive follow-up questions.
- **Strict Anti-Hallucination:** Specifically instructed to never guess. If information is missing from the video, it reliably outputs: "This topic is not covered in the video."
- **Native Multilingual Support:** Generates summaries and answers in English (default) or pure, formal Indian Languages without code-mixing.
- **Robust Error Handling:** Safely catches missing transcripts, invalid URLs, and unavailable videos, returning clean error messages to the user.

## 🏗️ Architecture & Data Flow

This application operates using a **Tool-First Prompt Architecture** orchestrated by OpenClaw's autonomous agent capabilities.

### 1. How the Transcript is Stored

When a user submits a link, the system fetches the transcript using `youtube-transcript-api`. To avoid redundant API calls and handle long videos, the **full transcript is cached locally as a `.txt` file** in a dedicated `.clawhub/cache/` directory, named by its YouTube Video ID.

### 2. How Context is Managed

To maintain strict token efficiency, the system implements **Smart Truncation**. When the transcript is initially fetched, only the first 15,000 characters are sent to the LLM's short-term session memory. The OpenClaw framework inherently manages this session memory, keeping different Telegram users completely isolated from one another.

### 3. How Questions are Answered

The bot operates in specific interaction modes. When a user asks a follow-up question, the LLM first checks its immediate session context.
If the transcript was truncated and the answer isn't readily available, the LLM is instructed to **silently execute `search_cache.py`**. This script searches the local `.txt` cache for relevant keywords and returns a 1,000-character window (500 characters before and after the keyword) to the LLM. The LLM then synthesizes this newly fetched context to answer the user.

## ⚖️ Design Trade-offs

Here is why this specific architecture was chosen:

- **Keyword Window Search vs. Vector Embeddings (RAG):**
  Instead of chunking the transcript and storing it in a vector database (like ChromaDB or Pinecone) with embeddings, this project uses local `.txt` caching paired with a Python-based keyword search window.
    - _Why:_ Vector databases introduce heavy external dependencies and operational overhead that are over-engineered for a single YouTube video's context. The local cache + text-window search provides an incredibly fast, token-efficient, and highly reliable context retrieval method without bloating the codebase.

- **Prompt-Based Multilingual Generation vs. Translation API Layer:**
  Instead of piping English outputs through a third-party translation API, the system uses the LLM's native multilingual capabilities enforced via strict prompt engineering (`AGENTS.md`).
    - _Why:_ This drastically reduces system latency, avoids the loss of technical context common in direct word-for-word API translations, and simplifies the architecture by removing external API dependencies.

- **Lightweight Title Fetching (oEmbed) vs. HTML Scraping:**
  The actual video title is fetched using YouTube's official, lightweight JSON oEmbed API rather than downloading and parsing the entire heavy HTML webpage.
    - _Why:_ This minimizes network latency and ensures the bot responds to the user as quickly as possible.

## ⚙️ Setup & Installation

**Prerequisites:** Python 3.8+, Node.js (for OpenClaw), and a Telegram Bot Token via BotFather.

1. **Clone the repository:**

    ```bash
    git clone <your-repo-link>
    cd <repo-name>
    ```

2. **Install Python Dependencies:**
    ```
    pip install youtube-transcript-api
    ```
3. **Configure OpenClaw:**
    - Ensure `fetch_transcript.py` and `search_cache.py` are in your OpenClaw workspace.
    - Verify `AGENTS.md` and `skills/fetch-youtube-transcript/SKILL.md` contain the strict execution guardrails.
    - Connect your Telegram bot via the OpenClaw configuration.

4. **Run the Bot:**
    - Start your OpenClaw instance and message your bot on Telegram!

## 📸 Example Screenshots

![Summary](https://i.ibb.co/nsfpJFpz/00.png)
![Translation](https://i.ibb.co/TDTqZpW1/01.png)
![Edge Handling](https://i.ibb.co/ymWPPqWt/02.png)
