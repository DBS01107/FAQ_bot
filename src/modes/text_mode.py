# src/modes/text_mode.py


from src.utils import detect_language
from src.faq_matcher import match_faq
from src.doc_searcher import search_document
from src.faq_manager import log_question, log_unanswered, check_and_update_faqs


def run_text_mode():
    while True:
        user_input = input("You: ").strip()
        if not user_input:
            print("⚠️ No input detected. Please try again.")
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Thank you! जय हिंद 🚩")
            break

        lang = detect_language(user_input)
        answer = match_faq(user_input, lang)

        if answer:
            print(f"Bot (from FAQ): {answer}")
            source = "FAQ"
        else:
            print("Bot: Let me check the official document... 📄")
            answer = search_document(user_input, lang)
            print(f"Bot (from document): {answer}")
            source = "DOC"
            if 'No relevant information' in answer:
                log_unanswered(user_input, lang)

        log_question(user_input, lang, source, answer)
        check_and_update_faqs()

def handle_query(user_input):
    lang = detect_language(user_input)
    answer = match_faq(user_input, lang)
    if answer:
        source = "FAQ"
    else:
        answer = search_document(user_input, lang)
        source = "DOC"
        if 'No relevant information' in answer:
            log_unanswered(user_input, lang)
    log_question(user_input, lang, source, answer)
    check_and_update_faqs()
    return  answer, source
