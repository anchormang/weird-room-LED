import os
import RPi.GPIO as GPIO
from flask import Flask, render_template, Response
import datetime

GPIO.setmode(GPIO.BCM)
dataPin = [i for i in range(2,28)]
for dp in dataPin:
	GPIO.setup(dp, GPIO.IN)
#	pull_up_down = GPIO.PUD_UP)

data =  []
now = datetime.datetime.now()
timeString = now.strftime("%Y-%m-%d-%H:%M")
templateData = {
	'title':'LED Web App',
	'time':timeString,
	'data':data
}

def getData():
	data=[]	
	for i,dp in enumerate(dataPin):			#what does this loop do? 
		data.append(GPIO.input(dataPin[i]))
	return data
	
app = Flask(__name__)

@app.route('/')

def index():
#	return 'hello world'
	now = datetime.datetime.now()
	timeString = now.strftime("%Y-%m-%d-%H:%M")
	data = getData()
	templateData =  {
		'title':'LED Web Controller',
		'time':timeString,
		'data':data
	}

	return render_template('led-webcontroller.html', **templateData)

@app.route('/dev')

def dev():
	data = getData()
	print(data)
	return 'This is a page under development!'


@app.route('/<actionid>')
#Handles requests from the web page (initiated by clicks, entering text, etc.)
#Returns OK 200 to confirm the request has been received
def handleRequest(actionid):
	print("Something Happened: {}".format(actionid))	#this prints on the server host (i think thats what it's called)
	return "OK 200"

if __name__ == '__main__':
	os.system("sudo rm -r ~/.cache/chromium/DefaultCache/*")
	app.run(debug = True, port = 5000, host = '0.0.0.0', threaded = True)
