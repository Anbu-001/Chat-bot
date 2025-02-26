from fastapi import FastAPI, File, UploadFile
import speech_recognition as sr
import os

app = FastAPI()

TEMP_AUDIO_PATH = "/tmp/uploaded_audio.wav"

def save_temp_wav(audio_file):
    """Save uploaded audio as a temporary WAV file and print debug info."""
    try:
        print(f"🟢 Receiving file: {audio_file.filename}")
        with open(TEMP_AUDIO_PATH, "wb") as f:
            f.write(audio_file.file.read())
        print(f"✅ File saved successfully: {TEMP_AUDIO_PATH}")
        return TEMP_AUDIO_PATH
    except Exception as e:
        print(f"❌ Error saving file: {str(e)}")
        raise ValueError(f"Error processing audio file: {str(e)}")

def recognize_speech(audio_path):
    """Convert speech from WAV file to text."""
    recognizer = sr.Recognizer()
    try:
        print(f"🔍 Processing audio file: {audio_path}")
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            print(f"✅ Recognized text: {text}")
            return text
    except sr.UnknownValueError:
        print("⚠️ Could not understand the audio.")
        return "Could not understand the audio."
    except sr.RequestError as e:
        print(f"❌ Speech recognition service error: {str(e)}")
        return f"Speech recognition service error: {str(e)}"
    except Exception as e:
        print(f"❌ Speech recognition failed: {str(e)}")
        return f"Speech recognition failed: {str(e)}"

@app.post("/speech-to-text/")
async def speech_to_text(file: UploadFile = File(...)):
    """API Endpoint: Convert speech to text from uploaded file."""
    try:
        wav_path = save_temp_wav(file)  # Save the file
        text = recognize_speech(wav_path)  # Convert to text
        return {"text": text}
    except ValueError as ve:
        return {"error": str(ve)}
    except Exception as e:
        return {"error": f"Internal server error: {str(e)}"}
