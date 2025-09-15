
# 🤖 Personal AI Agent (Streamlit)

A clean **Streamlit-based AI Agent** with a chat interface.  
It works **without any API key** using built-in slash commands, and can optionally connect to **OpenAI** for smarter responses.

---

## ✨ Features
- **Chat UI with memory** (Streamlit chat components)  
- **Slash Tools (no API key needed):**
  - `/search <query>` → Quick DuckDuckGo web search  
  - `/wiki <topic>` → Short Wikipedia summary  
  - `/summarize <url>` → Fetch + summarize a web page  
  - `/calc <expr>` → Calculator (e.g., `/calc (12.5*3)+7`)  
- **Optional OpenAI integration**:  
  - Plug in your `OPENAI_API_KEY` for normal chat + advanced summarization  
- **Dark theme UI** with sidebar settings & tooltips  
- **Extensible** → easy to add new tools (`tools/` folder)

---

## 📂 Project Structure
```
ai-agent/
├── app.py               # Streamlit app (main chat logic)
├── tools/               # Tool functions
│   ├── web.py           # Search, wiki, fetch_url
│   └── utils.py         # Summarizer & calculator
├── .streamlit/config.toml   # Dark theme
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart
```bash
# 1) Create & activate virtual environment
python -m venv .venv
.\.venv\Scriptsctivate   # Windows
source .venv/bin/activate  # Mac/Linux

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run Streamlit app
streamlit run app.py
```
App will open at → [http://localhost:8501](http://localhost:8501)

---

## 🔐 OpenAI (Optional)
To enable smart chat & better summarization:
1. Create a `.env` file in the project root:
```
OPENAI_API_KEY=sk-...your-key...
OPENAI_MODEL=gpt-4o-mini
```
2. Restart the app.

---

## 🧪 Example Commands
- `/search best chaat places in Milpitas`  
- `/wiki samosa`  
- `/summarize https://en.wikipedia.org/wiki/Milpitas,_California`  
- `/calc (2*(15+3))/5`  

---

## 📸 Screenshot
*(Add a screenshot of your running app here!)*  

---

## 🤝 Contributions
PRs and ideas for new tools are welcome — just add functions in `tools/` and wire them up in `app.py`.
