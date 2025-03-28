import os
import struct
import pyaudio
import pvporcupine
import speech_recognition as sr
import openai
from gtts import gTTS


def main():
    """
    1. Initialize Porcupine for wake word detection.
    2. After wake word, record user speech.
    3. Send text to GPT.
    4. Use TTS to speak the GPT response.
    5. Loop back to wake word detection.
    """

    # ========== CONFIG ==========
    # Replace with your actual Picovoice Access Key
    picovoice_access_key = os.getenv("PICOVOICE_API_KEY", "ZSLJLFCd+I7a0wOPRCRFrsSUNs9ZtEKvdNXtVTIXThBwN0IuelMGTg==")
    # Replace with your actual OpenAI Key
    openai_api_key = os.getenv("OPENAI_API_KEY", "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")

    # Built-in keyword "computer"
    keyword = "computer"
    sensitivity = 0.5

    # STT config
    recognizer = sr.Recognizer()

    # GPT config
    openai.api_key = openai_api_key
    gpt_model = "text-davinci-003"  # or another model like "gpt-3.5-turbo"

    # ========== SETUP PORCUPINE ==========
    porcupine = pvporcupine.create(
        access_key=picovoice_access_key,
        keywords=[keyword],
        sensitivities=[sensitivity]
    )

    # ========== SETUP MICROPHONE STREAM ==========
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print(f"Listening for wake word '{keyword}'... (Press Ctrl+C to exit)")

    try:
        while True:
            # 1. WAKE WORD DETECTION
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm_unpacked)

            if keyword_index >= 0:
                print(f"Wake word '{keyword}' detected!")
                # 2. CAPTURE USER SPEECH
                user_text = capture_user_speech(recognizer)
                if user_text:
                    print(f"User said: {user_text}")

                    # 3. GPT QUERY
                    gpt_reply = ask_gpt(user_text, gpt_model)
                    print(f"GPT response: {gpt_reply}")

                    # 4. TTS
                    speak_text(gpt_reply)
                else:
                    print("No user speech detected or recognition failed.")
                # Return to wake word detection
                print(f"Listening again for wake word '{keyword}'...")

    except KeyboardInterrupt:
        print("Exiting gracefully...")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()


def capture_user_speech(recognizer):
    """
    Records a short audio clip from the microphone after the wake word,
    then uses Google STT to convert speech to text.
    """
    with sr.Microphone() as source:
        print("Please speak your command or question...")
        audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        print("Transcribing...")

    try:
        # Use Google STT (online) to get text
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print(f"Could not request results from STT service: {e}")
    return None


def ask_gpt(prompt, model="text-davinci-003"):
    """
    Sends a text prompt to OpenAI GPT and returns the response text.
    """
    try:
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return "I'm sorry, I ran into an error with GPT."


def speak_text(text):
    """
    Convert text to speech using gTTS, then play the resulting mp3 file.
    """
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        os.system("mpg123 response.mp3")  # Or another command-line mp3 player
    except Exception as e:
        print(f"Error during TTS: {e}")


if __name__ == "__main__":
    main()
