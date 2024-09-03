import pyttsx3 
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import smtplib
import time
from bs4 import BeautifulSoup
import requests


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!")
    else:
        speak('Good Evening!')

    speak("All systems good to go.. At your service.")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing....")
        query = r.recognize_google(audio, language='en-in')
        print(f'You said: {query}\n') 


    except Exception as e:
        print("Could you please repeat that?")
        return "None"
    return query

programOn = True

def jokes():
    url = "https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit"
    response = requests.get(url)
    joke_data = response.json()

    if joke_data["type"] == "twopart":
        final = f'{joke_data["setup"]} {joke_data["delivery"]}'
    else:
        final = joke_data["joke"]

    speak(final)


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('email', 'password')
    server.sendmail('email', to, content)
    server.close()


if __name__ == "__main__":
    wish()
    while programOn:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("Wikipedia says")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            wb.open('www.youtube.com')

        elif 'open stack overflow' in query:
            wb.open('stackoverflow.com')

        elif 'open spotify' in query:
            os.system('spotify')
        
        elif 'open code' in query:
            os.system('code')
        
        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'thank you' in query:
            speak("My Pleasure!")
        
        elif 'a joke' in query:
            jokes()

        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                speak("Please type the email of the person you wanna send the email to.")
                to = input("Please type the email of the person you wanna send the email: ")
                sendEmail(to, content)
                speak("Email has been sent.")
            except Exception as e:
                print(e)
                speak("Sorry sir, I am not able to send the email at the moment.")
        
        elif 'stop' in query:
            speak("Shutting down systems. Thank you for your time.")
            break

        elif 'hold' in query:
            speak("Holding for 10 seconds")
            time.sleep(10)
            speak("I am back!")

        elif 'what can you do' in query:
            speak("I can do a lot of things! First of all, I can tell you about anyone from the wikipedia! after that, I can tell you the time and temperature and I can also start applications for you! I can send emails and to top it all off, I can tell you jokes!")

        elif 'the temperature' in query:
            speak("Please tell me where you are living in.")
            city = takeCommand()
            url = "https://www.google.com/search?q="+"weather"+city
            html = requests.get(url).content
            soup = BeautifulSoup(html, 'html.parser')
            temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
            str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
            data = str.split('\n')
            time = data[0]
            sky = data[1]

            listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
            strd = listdiv[5].text
            
            pos = strd.find('Wind')
            
            speak(f"Temperature is {temp}")
            speak(f"The sky description is {sky}")
