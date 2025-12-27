# Personal AI Assistant (V2)

A robust, modular, and safe AI assistant written in Python.

## 🛡️ strict Security Features
- **Sandboxed Filesystem**: All file creations are restricted to a `workspace/` directory.
- **Permission First**: No action is taken without explicit user confirmation.
- **No Persistence**: Does not run in the background.

## 🚀 Setup

1.  **Clone & Enter**:
    ```bash
    cd ai_assistant
    ```

2.  **Install**:
    ```bash
    python -m pip install -r requirements.txt
    ```

3.  **Config**:
    Create a `.env` file:
    ```ini
    OPENAI_API_KEY=your_key_here
    # Optional
    BASE_WORKSPACE_DIR=./workspace
    DRY_RUN=False
    ```

4.  **Run**:
    ```bash
    python -m ai_assistant.main
    ```

## 📝 Usage Examples

- **Open Website**: "Open google.com"
- **Open App**: "Open Notepad"
- **File System**: "Create folder Projects", "List files"
- **Chat**: "Tell me a joke"

## ⚠️ Disclaimer
This software is provided for educational purposes. Always review the code before providing API keys or executing commands on your machine.
