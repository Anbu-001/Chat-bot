import google.generativeai as genai
import speech_recognition as sr
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)  # Faster response
    
    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return ""
    except sr.RequestError:
        print("Could not request results, please check your internet connection.")
        return ""

def chat_with_gpt(prompt):
    genai.configure(api_key="*********************************")
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Respond concisely: {prompt}", stream=False)
    return response.text if hasattr(response, "text") else "I'm not sure, could you clarify?"

def main():
    speak("Hello! How can I assist you today?")
    while True:
        user_input = listen()
        if user_input.lower() in ["exit", "quit", "stop"]:
            speak("Goodbye!")
            break
        if user_input:
            response = chat_with_gpt(user_input)
            print("Bot:", response)
            speak(response)

if __name__ == "__main__":

    main()
