import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import time
import re

# Initialize the speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def greet_user():
    hour = datetime.datetime.now().hour
    if hour < 12:
        speak("Good morning!")
    elif 12 <= hour < 18:
        speak("Good afternoon!")
    else:
        speak("Good evening!")

def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for wake word...")
        while True:
            audio = recognizer.listen(source)
            try:
                command = recognizer.recognize_google(audio)
                print(f"You said: {command}")
                if "hey assistant" in command.lower():  # Change this to your desired wake word
                    speak("How can I assist you?")
                    return
                
            except sr.UnknownValueError:
                continue  # Ignore unrecognized speech
            except sr.RequestError:
                speak("Sorry, my speech service is down.")
                speak("Please connect to internet.")
                return

def listen_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        audio = recognizer.listen(source)
        command = ""
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
        except sr.RequestError:
            speak("Sorry, my speech service is down.")
        return command.lower()

def open_file(file_path):
    print(f"Attempting to open: {file_path}")  # Debugging output
    if os.path.exists(file_path):
        os.startfile(file_path)
        speak(f"Opening {file_path}")
    else:
        speak("Sorry, I could not find that file.")

def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    webbrowser.open(url)
    speak(f"Searching the web for {query}")

def set_reminder(reminder, duration):
    speak(f"Reminder set for {reminder} in {duration} seconds.")
    time.sleep(duration)  # Duration is already in seconds
    speak(f"Reminder: {reminder}")

def parse_reminder_command(command):
    # Regex to find the duration in minutes and seconds
    minutes_match = re.search(r'(\d+)\s*minutes?', command)
    seconds_match = re.search(r'(\d+)\s*seconds?', command)

    duration = 0

    if minutes_match:
        duration += int(minutes_match.group(1)) * 60  # Convert minutes to seconds

    if seconds_match:
        duration += int(seconds_match.group(1))  # Add seconds

    if duration > 0:
        reminder = command.split('remind me to')[-1].strip()
        
        # Remove the found time phrases from the reminder
        if minutes_match:
            reminder = reminder.replace(minutes_match.group(0), '').strip()
        if seconds_match:
            reminder = reminder.replace(seconds_match.group(0), '').strip()

        return reminder, duration

    return None, None

def speak_current_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")  # Format the time
    speak(f"The current time is {current_time}")

def speak_current_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")  # Format the date
    speak(f"Today's date is {current_date}")

def search_youtube(query):
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Searching YouTube for {query}")

def main():
    greet_user()
    
    while True:
        listen_for_wake_word()  # Wait for the wake word
        command = listen_command()  # Listen for the actual command

        if 'open' in command:
            file_path = command.replace('open', '').strip()
            open_file(file_path)
        elif 'search' in command:
            query = command.replace('search', '').strip()
            search_web(query)
        elif 'remind me to' in command:
            reminder, duration = parse_reminder_command(command)
            if reminder and duration is not None:
                set_reminder(reminder, duration)
            else:
                speak("I couldn't understand the reminder time. Please specify the duration in minutes and seconds.")
        elif 'what time is it' in command:
            speak_current_time()
        elif 'what is the date' in command:
            speak_current_date()
        elif 'youtube' in command:
            query = command.replace('youtube', '').strip()
            search_youtube(query)
        elif 'goodbye' in command:
            speak("Goodbye!")
            break
        else:
            speak("")

if __name__ == "__main__":
    main()