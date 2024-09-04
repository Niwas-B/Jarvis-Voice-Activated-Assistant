import os
from gtts import gTTS
import pygame
import webbrowser
import speech_recognition as sr
import pyttsx3
import requests
import musicLib



recognizer= sr.Recognizer()
engine= pyttsx3.init()
newsApiKey = "3d2a917b1fb34281bb40dc579d37fb09"

def speak (text):
    if os.path.exists("speech.mp3"):

        os.remove("speech.mp3")
    
    # Convert the text to speech and save it to an MP3 file
    tts = gTTS(text=text, lang='en')
    tts.save("speech.mp3")  
    
    # Initialize pygame mixer (if not already initialized)
    if not pygame.mixer.get_init():
        pygame.mixer.init()
        
    pygame.mixer.music.load("speech.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    

def processCmd ( c):
    if("open google" in c.lower()):
        webbrowser.open("https://google.com")
    elif ("open facebook"in c.lower()):
        webbrowser.open("https://facebook.com")
    elif ("open youtube"in c.lower()):
        webbrowser.open("https://youtube.com")
    elif (c.lower().startswith("play")):
        song= c.lower().split(" ")[1]
        link = musicLib.music[song]
        webbrowser.open(link)
    elif "exit" in c.lower():
        print("Exiting Jarvis...")
        speak("Goodbye!")
        return False
    
    elif "news" in c.lower():
        r= requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsApiKey}",timeout=10)
        headlines = r.json().get('articles', [])

        for i, article in enumerate(headlines, 1):
            speak(f"{i}. {article['title']}")
    else :
        print(c)
        speak("can't proceed with the command")


if __name__== "__main__":
    print("Initializing Jarvis...")
    speak("Jarvis, initialized!")
    

    while True:  
        try:
            with sr.Microphone() as source:
            
                audio_text = recognizer.listen(source,timeout= 2)
                
        # using google speech recognition
                audio = recognizer.recognize_google(audio_text)
                print(audio)
                if(audio.lower()=="jarvis"):
                    print ( "Jarvis Active...")
                    print("How may I help You?")
                    speak("How may I help You?")
                    with sr.Microphone() as source :
                    
                        audio= recognizer.listen(source,timeout= 3)
                        command = recognizer.recognize_google(audio)

                        processCmd(command)

                elif "exit" in audio.lower():
                    print("Exiting Jarvis...")
                    speak("Goodbye!")
                    break

        except sr.UnknownValueError:
            speak("Sorry, I did not get that.")
        except Exception as e:
            speak("Sorry, I did not get that")
            print(f"Error; {e}")