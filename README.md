# 🤖 Recruitment FAQ Chatbot (English/मराठी)

An intelligent chatbot designed to answer recruitment FAQs in both English and Marathi, with voice and text-based interaction via a user-friendly web interface powered by Streamlit.

## ✨ Features

✅ Multilingual support (English and Marathi)  
✅ Voice and text-based conversation modes  
✅ Automatic language detection  
✅ FAQ matching with fallback document-based search  
✅ Dynamic FAQ management — frequently asked questions are auto-added to the FAQ database  
✅ Detailed query logging with timestamp, frequency, and source  
✅ Audio output directly in the web app  
✅ Seamless UI using Streamlit

## 🗂 Directory Structure

├── app/
│ └── viewer.py # Streamlit web application
├── data/ # FAQs, logs, unanswered questions
├── model/ # Document embeddings cache
├── src/
│ ├── modes/ # audio_mode.py, text_mode.py
│ ├── utils.py # language detection, helpers
│ ├── faq_manager.py # logging & FAQ updates
│ ├── faq_matcher.py # semantic FAQ matching
│ └── doc_searcher.py # official document search
├── tests/ # test scripts
├── README.md
└── requirements.txt


## 🚀 How to Run

    ### 1️⃣ Install dependencies

        Make sure you’re in a virtual environment or your preferred Python setup, then run:

        ```bash
        pip install -r requirements.txt
        ```

    ### 2️⃣ Run the chatbot app

        ```bash
        streamlit run app/viewer.py
        ```
        The app will launch on http://localhost:8501.

## 🗣 Usage

    Choose between text input or voice mode.

    Type your question or press the Record button to speak.

    The bot will respond using relevant FAQs or fallback to searching official documents.

    Answers are shown on screen and played back as audio.

    All queries are logged with details to improve FAQ coverage automatically.

## 📊 Data Files
    asked_questions_log.csv: Tracks every query with timestamp, language, question, source, answer, and frequency.

    unanswered_questions.csv: Stores queries that couldn’t be answered.

    TES_54_FAQs.xlsx / TES_54_FAQs_Marathi.xlsx: English and Marathi FAQs.

    document_cache.pkl: Cached document embeddings for fast retrieval.

## 📚 Technologies Used
    Python 3.12+

    Streamlit for interactive UI

    HuggingFace Transformers for semantic search

    SpeechRecognition and pyttsx3/gTTS for voice features

    Pandas for data processing


