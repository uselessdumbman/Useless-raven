import speech_recognition as sr
import wikipedia as wiki
import os
import webbrowser
import datetime as dt
import pyttsx3 as py
import requests
import re

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = py.init("sapi5")
voices = engine.getProperty('voices')
engine.setProperty("voice", voices[1].id)

# Function to make the assistant speak
def say(text):
    engine.say(text)
    engine.runAndWait()

# Function to query an AI model (assuming you have the correct API endpoint and token)
def ai(prompt):
    say("any thhing else my friend")
    API_URL = "https://api-inference.huggingface.co/models/google/gemma-1.1-7b-it"
    headers = {"Authorization": "Bearer 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"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({"inputs": prompt})
    text = output[0]['generated_text']
    say(text)
    sc(prompt, text)  # Pass the response to the sc function for saving

# Function to save conversation logs
def sc(prompt, response):
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    sanitized_prompt = re.sub(r'[^\w\s-]', '', prompt).strip().replace(' ', '_')
    filename = f"Openai/{sanitized_prompt}.txt"

    with open(filename, "w") as f:
        f.write(f"master said: {prompt}\n")
        f.write(f"raven said: {response}\n")

# Function to take voice commands
def takecommand():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        query = recognizer.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        return query

# Main loop to handle commands
if __name__ == "__main__":
    while True:
        say("Hello, I am Raven.")
        print("Listening....")
        query = takecommand().lower()

        if query:
            say(f"You said: {query}")

            sites = {
                "youtube": "https://www.youtube.com/",
                "wikipedia": "https://en.wikipedia.org/wiki/Wikipedia",
                "hello": "https://www.pw.live/study/batches/study",
                "google": "https://www.google.com/"
            }

            for site in sites:
                if f"open {site}" in query:
                    say(f"Opening {site}")
                    webbrowser.open(sites[site])
                    break

            if "open music" in query:
                say("Please enter the song name")
                songname = takecommand().lower()
                musicpath = f"C:\\Users\\Stupid man\\Music\\goldfire\\{songname}.mp3"
                os.system(f'start "" "{musicpath}"')

            if "tell the time" in query:
                time = dt.datetime.now().strftime("%H:%M %S")
                say(f"Sir, the time is {time}")

            if "open app" in query:
                say("Please enter the app name")
                appname = takecommand().capitalize()
                apppath = f"C:\\Users\\Stupid man\\AppData\\Local\\Microsoft\\WindowsApps\\{appname}.exe"
                os.system(f'start "" "{apppath}"')

            if " raven" in query:
                ai(prompt=query)
