import os
import csv
from datetime import datetime
import pandas as pd
from src.faq_matcher import match_faq, faq_data
from src.utils import detect_language
from src.doc_searcher import search_document

# Paths
FAQ_PATHS = {
    'en': 'data/TES_54_FAQs.xlsx',
    'mr': 'data/TES_54_FAQs_Marathi.xlsx'
}
LOG_PATH = "data/asked_questions_log.csv"
UNANSWERED_PATH = "data/unanswered_questions.csv"
THRESHOLD = 3  # Promote to FAQ after 3 document hits

# Ensure log files exist
for path, header in [
    (LOG_PATH, ['timestamp', 'lang', 'question', 'source', 'answer', 'frequency']),
    (UNANSWERED_PATH, ['timestamp', 'lang', 'question'])
]:
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(header)


def get_updated_frequency(query):
    try:
        df = pd.read_csv(LOG_PATH)
        return df[df['question'] == query].shape[0] + 1
    except Exception:
        return 1


def log_question(query, lang, source, answer):
    cleaned_answer = (
        answer[:200].replace("\n", " ").replace("[1m", "").replace("[0m", "")
    )

    # Read existing log
    if os.path.exists(LOG_PATH):
        df = pd.read_csv(LOG_PATH)
    else:
        df = pd.DataFrame(columns=['timestamp', 'lang', 'question', 'source', 'answer', 'frequency'])

    # Normalize query for comparison (case-insensitive match)
    mask = df['question'].str.lower() == query.lower()

    if mask.any():
        # Update the most recent matching row
        index = df[mask].index[-1]
        df.at[index, 'frequency'] += 1
        df.at[index, 'timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        df.at[index, 'source'] = source
        df.at[index, 'answer'] = cleaned_answer
    else:
        # Add new row
        new_row = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'lang': lang,
            'question': query,
            'source': source,
            'answer': cleaned_answer,
            'frequency': 1
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

    # Save updated log
    df.to_csv(LOG_PATH, index=False, quoting=csv.QUOTE_ALL)



def log_unanswered(query, lang):
    with open(UNANSWERED_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lang,
            query
        ])


def check_and_update_faqs():
    df = pd.read_csv(LOG_PATH)
    freq = df[df['source'] == 'DOC']['question'].value_counts()
    to_promote = freq[freq >= THRESHOLD].index.tolist()

    if not to_promote:
        return

    for lang, path in FAQ_PATHS.items():
        df_faq = pd.read_excel(path)
        q_col, a_col = ('Question', 'Answer') if lang == 'en' else ('प्रश्न', 'उत्तर')

        for q in to_promote:
            if q not in df_faq[q_col].values:
                df_faq = pd.concat([df_faq, pd.DataFrame([{q_col: q, a_col: ''}])], ignore_index=True)
                print(f"[INFO] ✅ Auto-added new FAQ: '{q}' in {lang.upper()} FAQ")

        df_faq.to_excel(path, index=False)
