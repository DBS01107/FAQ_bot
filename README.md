# 🤖 Recruitment FAQ Chatbot (English / मराठी)

A bilingual (English and Marathi) FAQ chatbot that answers user queries related to recruitment using:
- A curated FAQ dataset.
- Document search for fallback.
- Language detection.
- Auto-logging and FAQ updating mechanisms.

---

## 📁 Project Structure

FAQ_chatbot/
├── data/ # FAQs, logs, and document files
├── model/ # Saved models or vector stores
├── src/ |
│ ├── faq_matcher.py # Matches questions against FAQs
│ ├── doc_searcher.py # Searches documents for fallback answers
│ ├── faq_manager.py # Logs, tracks, and promotes unanswered questions
│ ├── utils.py # Language detection and helper functions
│ └── main.py # Entry point for the chatbot
├── tests/ # (Optional) Unit tests
├── README.md # Project overview
└── requirements.txt # Python dependencies

---

## 🚀 Features

- ✅ Supports **English and Marathi** inputs.
- ✅ Matches questions to a predefined FAQ set.
- ✅ Falls back to **document search** when FAQs fail.
- ✅ **Logs** every user question for analysis.
- ✅ Automatically promotes frequently asked document-based questions to FAQ.
- ✅ CLI-based interaction.

---

