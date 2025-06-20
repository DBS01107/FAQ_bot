from faq_matcher import match_faq
from doc_searcher import search_document
from utils import detect_language
import sys
import csv
from datetime import datetime
from faq_manager import log_question, log_unanswered, check_and_update_faqs



def main():
    print("📢 Recruitment FAQ Chatbot (English / मराठी)")
    print("Type 'exit' to quit\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Bot: Thank you! जय हिंद 🚩")
            break

        lang = detect_language(user_input)

        answer = match_faq(user_input, lang)
        def log_question(query, lang, source, answer):
            with open("data/asked_questions_log.csv", "a", newline='', encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    lang,
                    query,
                    source,
                    answer[:200].replace("\n", " ")  # short version of answer
                ])

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

        # Log the question
        log_question(user_input, lang, source, answer)

        # Check if any document-based Qs should be promoted to FAQ
        check_and_update_faqs()

if __name__ == "__main__":
    main()
