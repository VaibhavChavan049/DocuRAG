# RAG Chatbot using OpenAI and Langchain

This chatbot will answer the question related to pdf that you upload.

## How to run the code locally

**Step 1:**

Run the following command in the command prompt to initiate the git operations

```
git init
```

**Step 2:**

Run the following command in the command promt to clone this repository

```
git clone https://github.com/VaibhavChavan049/RAG-Chatbot-using-Ollama-and-Langchain.git
```

**Step 3:**

Download Ollama using the following link:

https://ollama.com/

**Step 4:**

Run the following commands in the command prompt to download the required embedding and llm
```
ollama run qwen2.5:0.5b
```
```
ollama run granite-embedding:30m
```

**Step 5:**

Run the following command in the command prompt to run the chatbot app

```
streamlit run app.py
```

