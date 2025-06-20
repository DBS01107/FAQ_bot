import os
import re
import pdfplumber
from sentence_transformers import SentenceTransformer, util

import pickle

CACHE_PATH = "model/document_cache.pkl"


# Load the model once
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Global cache
doc_chunks = []
doc_embeddings = None

def load_pdf_chunks(pdf_path="data/notification.pdf"):
    global doc_chunks, doc_embeddings

    # Load from cache if exists
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            doc_chunks, doc_embeddings = pickle.load(f)
        return

    with pdfplumber.open(pdf_path) as pdf:
        full_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                full_text += page_text + "\n"

    lines = re.split(r'\n+', full_text)
    preprocessed_lines = []
    buffer = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.endswith(":") or line.isupper() or len(line.split()) <= 4:
            if buffer:
                preprocessed_lines.append(buffer.strip())
                buffer = ""
            buffer += line + " "
        else:
            buffer += line + " "

    if buffer:
        preprocessed_lines.append(buffer.strip())

    cleaned_chunks = list(set([
        chunk.strip() for chunk in preprocessed_lines
        if len(chunk.strip()) > 30
    ]))

    doc_chunks = cleaned_chunks
    doc_embeddings = model.encode(doc_chunks, convert_to_tensor=True)

    # Save to cache
    with open(CACHE_PATH, "wb") as f:
        pickle.dump((doc_chunks, doc_embeddings), f)
    print(f"Loaded {len(doc_chunks)} document chunks from {pdf_path}")


def keyword_fallback(query):
    query = query.lower()
    keywords = [word.strip("?:,.'\"") for word in query.split() if word.isalnum()]

    for chunk in doc_chunks:
        if all(k in chunk.lower() for k in keywords):
            return f"(Keyword match)\n{chunk}"
    return None

def highlight_keywords(text, query):
    keywords = [re.escape(word) for word in query.lower().split()]
    pattern = re.compile(r'\b(' + '|'.join(keywords) + r')\b', flags=re.IGNORECASE)
    return pattern.sub(r'\033[1m\1\033[0m', text)  # Bold highlight in terminal

def search_document(query, lang_code='en'):
    load_pdf_chunks()

    query_embedding = model.encode(query, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]
    best_match_idx = similarities.argmax().item()
    best_score = similarities[best_match_idx].item()

    # Threshold check
    if best_score > 0.6:
        best_chunk = doc_chunks[best_match_idx]
        return highlight_keywords(best_chunk, query)
    else:
        # Try keyword fallback
        fallback = keyword_fallback(query)
        if fallback:
            return highlight_keywords(fallback, query)
        else:
            return "No relevant information found in the official document."
