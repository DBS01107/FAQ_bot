from langdetect import detect

def detect_language(text):
    try:
        lang = detect(text)
        return 'mr' if lang == 'mr' else 'en'
    except:
        return 'en'
