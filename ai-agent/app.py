import os
import streamlit as st
from dotenv import load_dotenv
from tools import ddg_search, wiki_summary, fetch_url, summarize_text, calc_eval

load_dotenv()

st.set_page_config(page_title="Personal AI Agent", page_icon="🤖", layout="wide")

st.title("🤖 Personal AI Agent")
st.caption("Chat with tools. Works offline with /commands. Optional OpenAI for smart replies.")

with st.sidebar:
    st.subheader("Settings")
    api_key = st.text_input("OpenAI API Key (optional)", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    model = st.text_input("Model", value=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    st.markdown("**Slash Commands**\n- `/search <query>`\n- `/wiki <topic>`\n- `/summarize <url>`\n- `/calc <expr>`")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Hi! Ask me anything. Try /search or /wiki."}]

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

prompt = st.chat_input("Type a message or a /command…")
if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"):
        st.write(prompt)

    reply = None

    if prompt.startswith("/search "):
        q = prompt[len("/search "):].strip()
        results = ddg_search(q, max_results=5)
        reply = "\n\n".join([f"**{r['title']}**\n{r['href']}\n{r['body']}" for r in results]) or "No results."

    elif prompt.startswith("/wiki "):
        topic = prompt[len("/wiki "):].strip()
        reply = wiki_summary(topic, sentences=3)

    elif prompt.startswith("/summarize "):
        url = prompt[len("/summarize "):].strip()
        text = fetch_url(url)
        # fallback local summarizer; if user provided key, try LLM
        if api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                prompt_t = f"Summarize the following page in bullet points:\n\n{text[:6000]}"
                resp = client.chat.completions.create(model=model, messages=[{"role":"user","content":prompt_t}], temperature=0.2)
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = "(LLM unavailable) " + summarize_text(text)
        else:
            reply = summarize_text(text)

    elif prompt.startswith("/calc "):
        expr = prompt[len("/calc "):].strip()
        reply = calc_eval(expr)

    else:
        if api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                sys = "You are a concise helpful assistant. If a query looks like a web/topic lookup, suggest /search or /wiki."
                msgs = [{"role":"system","content":sys}] + [
                    {"role":m["role"],"content":m["content"]} for m in st.session_state.messages if m["role"]!="assistant"
                ]
                resp = client.chat.completions.create(model=model, messages=msgs, temperature=0.2)
                reply = resp.choices[0].message.content
            except Exception as e:
                reply = f"LLM error: {e}. You can still use /search, /wiki, /summarize, /calc."
        else:
            reply = "No API key set. Use /search, /wiki, /summarize <url>, or /calc."

    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"):
        st.write(reply)
