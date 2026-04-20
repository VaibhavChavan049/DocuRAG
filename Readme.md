# DocuRAG : AI-Powered Document Question Answering

Ask anything about your PDF documents using natural language — powered by local AI (Ollama + LangChain + Streamlit). No cloud, no API costs, full privacy.

---

## What it does

- Upload any PDF document
- Ask questions in plain English
- Get accurate answers based on the document content only

---

## Tech Stack

| Component | Technology |
|---|---|
| Web Framework | Streamlit |
| LLM | qwen2.5:0.5b (via Ollama) |
| Embeddings | granite-embedding:30m (via Ollama) |
| Vector Store | FAISS |
| RAG Pipeline | LangChain |

---

## How to run locally

**Step 1 — Clone the repository**
```bash
git clone https://github.com/VaibhavChavan049/DocuRAG.git
cd DocuRAG
```

**Step 2 — Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3 — Install Ollama**

Download and install from: https://ollama.com/

**Step 4 — Pull required models**
```bash
ollama pull qwen2.5:0.5b
ollama pull granite-embedding:30m
```

**Step 5 — Run the app**
``````````````````````````````````````````````````` at:``````````````````````````````````````````````````` at:``````````````````````````````````````````````````` at:`````````````````````````````````````````````he ``ght``````````````k **Ask DocuRAG** to get your answer
5. Click **Clear** to reset and ask a new question
