import tempfile
import time
import ollama
from gtts import gTTS
import subprocess
import speech_recognition as sr
import re
from gpiozero import LED
from gpiozero import Servo
from time import sleep


led = LED(26)
servo = Servo(17)

Talk=True

def speak(text):
    if text:
        try:
            tts = gTTS(text=text, lang='en')
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                tts.save(temp_file.name)
                subprocess.run(["mpg321", temp_file.name])
        except Exception as e:
            print("exception")



def get_responses(question):
    combined_answer = ""
    stream = ollama.chat(
        model='phi',
        messages=[{'role': 'user', 'content': question}],
        stream=True
    )
    for chunk in stream:
        message = chunk['message']['content']
        # print("Received chunk:", message)
        combined_answer += message
        print(combined_answer)
        # Check if the received message ends with a comma or period
        if message.endswith(',') or message.endswith('.'):
            # Speak the combined answer and reset it
            speak(combined_answer)
            combined_answer = ""
    # Speak any remaining text if it's not empty
    if combined_answer:
        # speak(combined_answer)
        speak("You can ask me another question now")



# Initialize the recognizer
recognizer = sr.Recognizer()

# Function to listen to audio and print recognized words
def listen_and_print():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        # Use the recognizer to convert speech to text
        words = recognizer.recognize_google(audio)
        print("You said:", words)
        return words.lower()
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        # speak("Sorry, could not understand audio.")
        return " "
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
        speak("Could not request result")
        return " "

# Call the function
while Talk:
    question = listen_and_print()
    if "hey jarvis" in question:
        print("HEY JARVIS")
        speak("Ask me a question")
        question = listen_and_print()
        if question!=" ":
            # if "servo" in question or "light" in question:
            #     if "servo" in question:
            #         speak("rotating servo")
            #         servo.min()
            #         sleep(1)
            #         # servo.mid()
            #         # sleep(1)
            #         servo.max()
            #         sleep(1)
            #         print("rotating servo")
            #     if "light" in question:
            #         if "on" in question:
            #             speak('turning light on')
            #             led.on()
            #             print("turned light on")
            #         else:
            #             speak('turning light off')
            #             led.off()
            #             print("turned light off")
            # else:    
            speak("finding answer please wait")
            get_responses(question)
        else:
            speak("Timeout")
    if "exit" in question:
        print("EXIT")
        break
    

