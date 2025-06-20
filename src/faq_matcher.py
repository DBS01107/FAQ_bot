import pandas as pd
from sentence_transformers import SentenceTransformer, util
from sklearn.metrics.pairwise import cosine_similarity
import os

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Multilingual-friendly

# Load FAQs at start
def load_faqs():
    eng_path = os.path.join("data", "TES_54_FAQs.xlsx")
    mar_path = os.path.join("data", "TES_54_FAQs_Marathi.xlsx")

    df_eng = pd.read_excel(eng_path)
    df_mar = pd.read_excel(mar_path)

    return {
        "en": {
            "questions": df_eng['Question'].tolist(),
            "answers": df_eng['Answer'].tolist(),
            "embeddings": model.encode(df_eng['Question'].tolist(), convert_to_tensor=True)
        },
        "mr": {
            "questions": df_mar['प्रश्न'].tolist(),
            "answers": df_mar['उत्तर'].tolist(),
            "embeddings": model.encode(df_mar['प्रश्न'].tolist(), convert_to_tensor=True)
        }
    }

faq_data = load_faqs()

def match_faq(query, lang_code):
    if lang_code not in faq_data:
        lang_code = 'en'  # fallback

    query_embedding = model.encode(query, convert_to_tensor=True)
    embeddings = faq_data[lang_code]['embeddings']

    # Use cosine similarity
    similarity_scores = util.pytorch_cos_sim(query_embedding, embeddings)[0]
    best_match_idx = similarity_scores.argmax().item()
    best_score = similarity_scores[best_match_idx].item()

    # Set a reasonable threshold to avoid false positives
    if best_score > 0.65:
        return faq_data[lang_code]['answers'][best_match_idx]
    else:
        return None
