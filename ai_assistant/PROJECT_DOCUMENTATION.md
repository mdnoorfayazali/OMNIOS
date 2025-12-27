# 🤖 Personal AI Assistant (V2) - Hackathon Edition

> **Team Omnios**: Building the future of Agentic AI.

## 🚀 The Vision
Development is fragmented. We switch constantly between terminals, browsers, and IDEs, losing context every time.
**Personal AI Assistant V2** is a multimodal, standout terminal agent that bridges these worlds. It doesn't just run commands; it **sees** your screen, **knows** the web, and **acts** on your capability.

---

## ✨ Key Features (The "Wow" Factor)

### 1. 👁️ Omni-Vision (Multimodal Analysis)
*   **Problem**: Terminal errors are cryptic.
*   **Solution**: "Analyze this screen."
*   **Tech**: Captures your screen using `pyautogui`, processes it with `Pillow`, and sends it to the Vision Model (GPT-4o) for instant context-aware analysis.

### 2. 🌐 Real-Time Web Agent
*   **Problem**: AI models have cutoff dates.
*   **Solution**: "Who won the game last night?"
*   **Tech**: Integrated `DuckDuckGo Search` allows the assistant to fetch live data from the web, summarizing results instantly.

### 3. 🛡️ Secure System Control
*   **Problem**: CLIs are rigid.
*   **Solution**: Natural language control. "Close Spotify", "Lock my screen", "Open the project folder."
*   **Tech**: Safe execution sandbox in `executor/actions.py` ensuring no accidental damage (e.g., directory traversal protection).

### 4. 🎨 Premium Terminal UI
*   **Aesthetic**: Built with `Ref` library.
*   **Experience**: Beautiful status panels, spinners, and startup animations that look like a sci-fi interface.

---

## 🛠️ Tech Stack
*   **Language**: Python 3.11+
*   **Core**: OpenAI API (GPT-4o)
*   **Interface**: Rich (TUI), Typer (CLI)
*   **Vision**: PyAutoGUI, Pillow
*   **Web**: DuckDuckGo Search
*   **Audio**: SpeechRecognition, PyAudio, pyttsx3

---

## ⚡ Quick Start

### 1. Installation
```bash
git clone https://github.com/your-repo/ai-assistant.git
cd ai-assistant
python -m pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file:
```ini
OPENAI_API_KEY=sk-your-key-here
```

### 3. Run
```bash
python -m ai_assistant.main --voice
```
*(Remove `--voice` for text-only mode)*

---

## 🗣️ Commands to Try (Demo Script)
1.  **"What is on my screen?"** (Tests Vision)
2.  **"Search for the latest Hackathon trends."** (Tests Web)
3.  **"Open Notepad and write 'Hello World'."** (Tests Automation)
4.  **"System status."** (Tests UI)
