import os
import time
import playsound
import speech_recognition as sr
import urllib3 
from gtts import gTTS
hello = False
def speak(text):
	tts = gTTS(text=text , lang = "en" , slow = False )
	filename = str("voice.mp3")
	tts.save(filename)
	playsound.playsound(filename , True)
def get_audio():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		audio = r.listen(source)
		said = ""

		try:
			said = r.recognize_google(audio)
			print(said)
		except Exception as e :
			print("Exception: " + str(e) )
	return said


while True:
	text = get_audio()
	if "Hey John" in text:
		speak("Hello , i am at your service")
		hello = True

	if hello == True :
		if "what's your name"  in text:
			speak("My Name Is Jarvis")
	if "Security" in text:
		os.system('python test.py')