## Getting Started

### 1. Install Ollama
Download and install Ollama from [ollama.com](https://ollama.com), then make sure it's running.

### 2. Download a chat model
I built this project with **qwen3:0.6b** because of my laptop's hardware limits. If your system has more RAM or a GPU, you can use a larger model for better responses:

```bash
ollama pull qwen3:0.6b    # lightweight, runs on most laptops
ollama pull qwen3:1.7b    # better quality, needs ~8 GB RAM
ollama pull qwen3:4b      # stronger, needs ~16 GB RAM
```

You can use any model from the [Ollama library](https://ollama.com/library) that supports tool calling.

### 3. Download an embedding model
The project also needs an embedding model to create vector embeddings:

```bash
ollama pull nomic-embed-text
```

### 4. Fork and clone the repo
Fork this repository, then clone your fork:

```bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>
```

### 5. Set up a virtual environment
```bash
python -m venv .venv

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Mac/Linux
source .venv/bin/activate

pip install -r requirements.txt
```


Change `MODEL` to whichever chat model you pulled in step 2.

### 6. Run the chatbot
```bash
python simple_ai_assistant.py
```

Type your message at the `User:` prompt. Type `exit` to quit.
