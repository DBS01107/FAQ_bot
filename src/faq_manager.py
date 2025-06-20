import os
import csv
from datetime import datetime
import pandas as pd
from faq_matcher import match_faq, faq_data 
from utils import detect_language
from doc_searcher import search_document


# Paths
FAQ_PATHS = {
    'en': 'data/TES_54_FAQs.xlsx',
    'mr': 'data/TES_54_FAQs_Marathi.xlsx'
}
LOG_PATH = "data/asked_questions_log.csv"
UNANSWERED_PATH = "data/unanswered_questions.csv"
THRESHOLD = 3  # frequency threshold to auto-add to FAQs

# Ensure log files exist
for path, header in [(LOG_PATH, ['timestamp','lang','question','source','answer','frequency']),
                     (UNANSWERED_PATH, ['timestamp','lang','question'])]:
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)


def get_updated_frequency(query):
    try:
        df = pd.read_csv(LOG_PATH)
        return df[df['question'] == query].shape[0] + 1
    except Exception:
        return 1


def log_question(query, lang, source, answer):
    freq = get_updated_frequency(query)
    with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            lang,
            query,
            source,
            answer.replace('\n',' ')[:200],
            freq
        ])


def log_unanswered(query, lang):
    with open(UNANSWERED_PATH, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
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
        if lang == 'en':
            q_col, a_col = 'Question', 'Answer'
        else:
            q_col, a_col = 'प्रश्न', 'उत्तर'

        for q in to_promote:
            if q not in df_faq[q_col].values:
                df_faq = df_faq.append({q_col: q, a_col: ''}, ignore_index=True)
                print(f"[INFO] Auto-added new FAQ entry for '{q}' in {lang} file.")

        df_faq.to_excel(path, index=False)


if __name__ == '__main__':
    print("📢 Recruitment FAQ Chatbot (English / मराठी)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit','quit']:
            print("Bot: Thank you! जय हिंद 🚩")
            break

        lang = detect_language(user_input)
        answer = match_faq(user_input, lang)

        if answer:
            print(f"Bot (from FAQ): {answer}")
            source = 'FAQ'
        else:
            print("Bot: Let me check the official document... 📄")
            answer = search_document(user_input, lang)
            print(f"Bot (from document): {answer}")
            source = 'DOC'
            if 'No relevant information' in answer:
                log_unanswered(user_input, lang)

        log_question(user_input, lang, source, answer)
        check_and_update_faqs()
    
        