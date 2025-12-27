# Personal AI Assistant V2 - OmniOS

## 🚀 Concept
**OmniOS** is an intelligent, multimodal agent designed to reclaim developer focus. Unlike traditional screen-blind CLIs, OmniOS is context-aware. It sees what you see, browses the web for you, and automates mundane tasks, all from a beautiful, futuristic terminal interface.

## ✨ Key Features
- **Omni-Vision**: Instantly analyze errors, plots, or UI designs on your screen. Just ask, *"What is this error?"*
- **Web Agent**: Real-time access to the internet to answer specific queries like *"Latest Hackathon trends"*.
- **System Control**: Launch apps, manage files, and control system states (Shutdown/Lock) via natural language.
- **Voice Mode**: Hands-free interaction for when you're brainstorming or multitasking.
- **Secure Workspace**: All file operations are sandboxed to a safe directory to prevent accidental system damage.

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Brain**: OpenAI GPT-4o (via Custom Client acting as Brain)
- **Vision**: PyAutoGUI + Base64 Encoding
- **Knowledge**: DuckDuckGo Search (ddgs)
- **Interface**: Rich (Python Library) for TUI
- **Voice**: PyAudio + SpeechRecognition + pyttsx3

## 📦 Setup & Run

### Prerequisites
1. Python 3.10 or higher.
2. An OpenAI API Key (set in `.env`).

### Installation
```bash
# Clone the repo
git clone https://github.com/your-repo/omnios.git
cd omnios

# Install dependencies
pip install -r ai_assistant/requirements.txt
```

### Running the Agent
```bash
python run_assistant.py
```

## 🎮 Usage Guide
| Command Intent | Example Input |
| :--- | :--- |
| **Vision** | "What's wrong with this code on my screen?" |
| **Web Search** | "Search for Python dictionary performance tips" |
| **App Control** | "Open VS Code" / "Close Notepad" |
| **File I/O** | "Create a file called notes.txt" |
| **General Chat** | "Explain quantum computing briefly" |

## 🔮 Future Improvements
- **Local LLM Inference**: Running entirely offline for privacy.
- **Action Policies**: Complex workflows like "Organize my downloads folder".
- **GUI Automation**: Clicking buttons and filling forms based on vision.
