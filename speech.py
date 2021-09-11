import speech_recognition as sr
import pyttsx3 




def create_engine():
    """
    Create Speech engine 
    """
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    return engine 


def speak(engine, text):
    #print(text)
    engine.say(text)
    engine.runAndWait()

def takeCommand():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        #print("Listening...")
        audio=r.listen(source)

        try:
            statement=r.recognize_google(audio,language='es-ES')
            #print(f"TU: {statement}\n")

        except Exception as e:
            #speak("Disculpe, no lo entiendo")
            return "None"
        return statement






