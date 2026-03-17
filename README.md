# Hiya Chat Assistant Backend

## Overview
**Hiya Chat Assistant Backend** is a Python-based backend system designed to power an AI chat assistant.  
It manages chat requests, integrates with Large Language Models (LLMs), and stores user interaction data.

The backend follows a **modular architecture**, making it easy to maintain, extend, and integrate with frontend applications.

---

# Features
- AI-powered chat assistant backend
- Local LLM execution using **Ollama**
- Modular Python architecture
- Lightweight **SQLite database**
- Clean API layer for chat interactions
- Easy development setup

---

# Tech Stack

| Technology | Purpose |
|-----------|--------|
| Python 3.10+ | Core backend language |
| Flask | API server framework |
| SQLite | Lightweight database |
| Ollama | Local LLM runtime |
| Llama3 / Phi3 | AI models used for chat |

---

## Project Structure
```
agentic-ai-backend/
├── db.py         # Database connection and operations
├── main.py       # Entry point for running the application
├── model.py      # Data models and business logic
├── server.py     # Web server and API endpoints
├── __pycache__/  # Python cache files (auto-generated)
```

## Installation
1. **Clone the repository**
   ```sh
   git clone <repo-url>
   cd agentic-ai-backend
   ```
2. **Create a virtual environment (optional but recommended)**
   ```sh
   python -m venv venv
   venv\Scripts\activate   # On Windows
   source venv/bin/activate # On Linux/Mac
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
   If `requirements.txt` is missing, install Flask and SQLite:
   ```sh
   pip install flask
   ```

## Usage
- **Run the server**
  ```sh
  python server.py
  ```
- **Run the main application**
  ```sh
  python main.py
  ```

## File Explanations
- **db.py**: Handles database setup and queries.
- **main.py**: Main entry point; may initialize the app or run scripts.
- **model.py**: Contains data models and core logic for chat assistant.
- **server.py**: Sets up the web server and API routes for chat interactions.
- **resetdb.py**: Utility script to reset the SQLite database by dropping all user tables and clearing the `sqlite_sequence` table to ensure a clean development state.
- **__pycache__/**: Stores Python bytecode cache files (auto-generated).

## Flow (Step-by-Step)
1. **Start the server**: Launches the backend API for chat requests.
2. **User sends a chat request**: The server receives and processes the request.
3. **Model logic**: `model.py` processes the request, interacts with the database if needed.
4. **Database operations**: `db.py` manages data storage and retrieval.
5. **Response**: The server sends back a response to the user/client.

## Documentation
- Each file is commented for clarity.
- For detailed API usage, see the docstrings in `server.py` and `model.py`.
- For database schema, see `db.py`.

## Architecture
The backend is structured in a modular way:

1. **API Layer**: Handles incoming chat requests (server.py, model.py)
2. **LLM Integration**: Uses Ollama to run and serve LLMs (Llama3, Phi3)
3. **Database Layer**: Stores user profiles and chat history (db.py)

### Diagram
```
User / Client
      |
      v
API Server (server.py)
      |
      v
Model Logic (model.py)
      |
      v
LLM Model via Ollama
      |
      v
Database Storage (db.py)
```



## Ollama Installation & Usage

## LLM & Model Information
- **Ollama** is used to serve Large Language Models (LLMs).
- The backend pulls and runs models like **Llama3** and **Phi3** for chat intelligence.
- The model is selected and managed in `server.py` and `model.py`.
Ollama is a local server for running and serving large language models (LLMs) like Llama3 and Phi3. It allows you to run advanced AI models on your own machine and connect them to your backend.

### Why Ollama?
- Enables running LLMs locally without cloud dependencies
- Supports multiple open-source models
- Easy integration with Python backend

### How to Install Ollama (Windows)
1. Go to the official Ollama website: https://ollama.com/download
2. Download the Windows installer and run it.
3. By default, Ollama installs to:
   `C:\Users\<YourUser>\AppData\Local\Programs\Ollama\ollama.exe`
   (Update the path in `server.py` if your username or install location differs.)

### How to Run Ollama
Ollama is started automatically by the backend (`server.py`).
You can also run it manually:
```sh
C:\Users\<YourUser>\AppData\Local\Programs\Ollama\ollama.exe serve
```
To pull a model (e.g., Phi3):
```sh
C:\Users\<YourUser>\AppData\Local\Programs\Ollama\ollama.exe pull phi3
```

### Integration
The backend uses the OLLAMA_EXE path in `server.py` to start the Ollama server and pull the required model. Make sure the path matches your installation.

## Why SQLite?
SQLite is chosen for its simplicity and zero-configuration setup. It is lightweight, file-based, and ideal for prototyping or small-scale applications. It allows easy storage of user profiles and chat history without needing a separate database server.

**Advantages:**
- No server required
- Easy to set up and use
- Good for development and small production workloads

For larger scale, you can migrate to PostgreSQL or MySQL.

---

## License
MIT License

## Maintainer
Project maintained by the Hiya Chat Assistant development team.
For questions or support, please contact the repository maintainer.

