#description: this is a virtual assistant
#pip install pyaudio
#sudo pip install SpeechRecognition
#sudo pip install gTTS
#sudo pip install wikipedia

import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia
from playsound import playsound


#ignore any warnings
warnings.filterwarnings('ignore')

#record audio
def recordAudio():
	r=sr.Recognizer() #creating a recognizer obj
	#open the mic
	with sr.Microphone() as source:
		print("Say Something? I am Listeniing")
		audio=r.listen(source)

	#use googles speech recog
	data=''
	try:
		data=r.recognize_google(audio)
		print("You Said >> "+data)
	except sr.UnknownValueError:
		print("Google speech recogniton could not understand the audio, unknown error")
	except sr.RequesError as e:
		print("Request results from google Speech recogniton service error "+e)

	return data

def AssitantResponse(text):
	print(text)
	myobj=gTTS(text=text,lang='en',slow=False)
	#save the converted audio to file
	myobj.save('assistant_response.mp3')
	os.system("ffplay assistant_response.mp3")

# A function for wake wordss
def WakeWords(text):
	WAKE_WORDS=['hey computer','ok computer']
	text=text.lower()
	for phrase in WAKE_WORDS:
		if phrase in text:
			return True

	return False

def getDate():
	now=datetime.datetime.now()
	my_date=datetime.datetime.today()
	weekday=calendar.day_name[my_date.weekday()]
	monthnum=now.month
	dayNum=now.day
	month_names = ['January', 'February', 'March', ' April', 'May', 'June', 'July', 'August', 'September', ' October',
				   'November', 'December']
	ordinalNumbers = ['1st', '2nd', '3rd', ' 4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
					  '14th', '15th', '16th',
					  '17th', '18th', '19th', '20th', '21st', '22nd', '23rd', '24rd', '25th', '26th', '27th', '28th',
					  '29th', '30th', '31st']

	return "Today is "+weekday+" "+month_names[monthnum-1]+" the "+ordinalNumbers[dayNum-1]+"."

# a function to get a random greeting
def greeting(text):
	Greeting_inputs=["hi","hey",'greetings','wasssup','hello','namaste']
	Greeting_responses=["holla","hello","namaste","howdy","hello there"]
	#if user inputs a greeting then return a random greeting from the computer
	for word in text.split():
		if word.lower() in Greeting_inputs:
			return random.choice(Greeting_responses) +" ."

	return " "
# a function to get a persons last name and fisrt name from the text
def getPerson(text):
	wordList=text.split()
	for i in range(0,len(wordList)):
		if i+3<=len(wordList)-1 and wordList[i].lower()=="who" and wordList[i+1].lower()=="is":
			return wordList[i+2]+" "+wordList[i+3]

while True:
	#record the audio
	text=recordAudio()
	response=''
	#check for the wake word
	if(WakeWords(text)==True):
		#check for greeting by the user
		response=response+greeting(text)
		if 'date' in text:
			get_date=getDate()
			response=response+" "+get_date

		#check is the user has to do anything with time ?
		if('time' in text):
			now =datetime.datetime.now()
			meridem=" "
			if now.hour>=12:
				meridem="p.m"
				hour=now.hour-12
			else:
				meridem="a.m"
				hour=now.hour
			if now.minute<10:
				minute='0'+str(now.minute)
			else:
				minute=str(now.minute)
			response=response+" "+"It is "+str(hour)+" : "+minute+" "+meridem+"."

		#chekc if the the user said who is ?
	if('who is' in text):
		person=getPerson(text)
		wiki=wikipedia.summary(person, sentences=2)
		response=response+" "+wiki

		#let the assistant respoind
	AssitantResponse(response)
