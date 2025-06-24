# src/modes/audio_mode.py



from src.utils import detect_language
from src.faq_matcher import match_faq
from src.doc_searcher import search_document
from src.faq_manager import log_question, log_unanswered, check_and_update_faqs

import speech_recognition as sr
import pyttsx3
from gtts import gTTS
import tempfile


def speak_streamlit(text, lang_code='en'):
    import streamlit as st
    import base64

    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            # Read MP3 and encode to base64
            with open(tmpfile.name, "rb") as f:
                data = f.read()
                b64 = base64.b64encode(data).decode()
                audio_html = f"""
                <audio autoplay>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Audio playback failed: {e}")



recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

def speak(text):
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        query = recognizer.recognize_google(audio)
        print(f"You (via mic): {query}")
        return query
    except sr.UnknownValueError:
        print("⚠️ Sorry, could not understand.")
        return ""
    except sr.RequestError:
        print("🚫 Speech service is unavailable.")
        return ""





def run_audio_mode():
    speak("Voice mode activated. You can start speaking now.")
    
    while True:
        user_input = listen().strip()
        if not user_input:
            speak("I didn't catch that. Please try again.")
            continue

        if user_input.lower() in ["exit", "quit"]:
            speak("Thank you! Jai Hind!")
            print("Bot: Thank you! जय हिंद 🚩")
            break

        lang = detect_language(user_input)
        answer = match_faq(user_input, lang)

        if answer:
            print(f"Bot (from FAQ): {answer}")
            speak(answer)
            source = "FAQ"
        else:
            print("Bot: Let me check the official document... 📄")
            answer = search_document(user_input, lang)
            print(f"Bot (from document): {answer}")
            speak(answer)
            source = "DOC"
            if 'No relevant information' in answer:
                log_unanswered(user_input, lang)

        log_question(user_input, lang, source, answer)
        check_and_update_faqs()


def streamlit_voice_query():
    import streamlit as st
    with sr.Microphone() as source:
        st.info("🎙️ Listening... Please speak now.")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        query = recognizer.recognize_google(audio)
        st.success(f"You said: {query}")
    except sr.UnknownValueError:
        st.warning("⚠️ Could not understand.")
        return None, None
    except sr.RequestError:
        st.error("🚫 Speech recognition service unavailable.")
        return None, None

    # Use existing logic
    lang = detect_language(query)
    answer = match_faq(query, lang)
    source = "FAQ"

    if not answer:
        st.info("📄 Checking the official document...")
        answer = search_document(query, lang)
        source = "DOC"
        if 'No relevant information' in answer:
            log_unanswered(query, lang)

    log_question(query, lang, source, answer)
    check_and_update_faqs()
    speak_streamlit(answer, lang_code=lang)
    return answer, source
