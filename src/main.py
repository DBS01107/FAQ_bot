# src/main.py

from modes.text_mode import run_text_mode
from modes.audio_mode import run_audio_mode

def main():
    print("📢 Recruitment FAQ Chatbot (English / मराठी)")
    mode = input("Choose input mode - 🎙️ Voice (v) or 🧑‍💻 Text (t): ").strip().lower()

    if mode == 'v':
        run_audio_mode()
    else:
        run_text_mode()

if __name__ == "__main__":
    main()
