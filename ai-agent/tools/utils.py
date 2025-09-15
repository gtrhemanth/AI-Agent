import re

def clean_text(txt: str) -> str:
    return re.sub(r"\s+", " ", txt).strip()

def summarize_text(text: str, max_sentences: int = 5) -> str:
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if len(s.strip()) > 0]
    sents.sort(key=len, reverse=True)
    top = sents[:max_sentences]
    return " ".join(top) if top else text[:400]

def calc_eval(expr: str) -> str:
    if not re.fullmatch(r"[0-9+\-*/().\s]+", expr):
        return "Invalid characters in expression."
    try:
        return str(eval(expr, {"__builtins__": {}}, {}))
    except Exception as e:
        return f"Error: {e}"
