import speech_recognition as sr
import os
import webbrowser
import datetime

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        print("🌞 Good Morning!")
    elif hour >= 19:
        print("🌙 Good Night!")
    else:
        print("👋 good afternoon")

def perform_command(command):
    command = command.lower()

    if "open notepad" in command:
        print("Opening Notepad...")
        os.system("start notepad")

    elif "open calculator" in command:
        print("Opening Calculator...")
        os.system("start calc")

    elif "open google" in command:
        print("Opening Google...")
        webbrowser.open("https://www.google.com")

    elif "open gmail" in command:
        print("Opening Gmail...")
        webbrowser.open("https://mail.google.com")

    elif "open whatsapp" in command:
        print("Opening WhatsApp Web...")
        webbrowser.open("https://web.whatsapp.com")

    elif "shutdown" in command:
        confirm = input("Do you really want to shut down the computer? (yes/no): ")
        if confirm.lower() == "yes":
            print("Shutting down...")
            os.system("shutdown /s /t 1")
        else:
            print("Shutdown cancelled.")

    else:
        print("Command not recognized.")

# MAIN PROGRAM
greet_user()

r = sr.Recognizer()

with sr.Microphone() as source:
    print("🎙 Listening for your command...")
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)

try:
    command_text = r.recognize_google(audio)
    print("You said:", command_text)
    perform_command(command_text)

except sr.UnknownValueError:
    print("Sorry, I could not understand the audio.")
except sr.RequestError as e:
    print("Could not request results; check your internet connection.")