#installing packages (pip install speech recognition package)
#Need an internet connection for the application to work
#make a folder named weather_icons in the project and place all icons titled under "Icon List" from this link inside: https://openweathermap.org/weather-conditions (source of images)
import speech_recognition as sr
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import requests

def getspeechinput(recognizer, microphone):
    #Get mic input
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    #Catch errors and set outputstring to empty string if there is, so there will be no GUI displays when the function is called in ready and checked with selection
    #uses google api to recognize audio
    try:
        outputstring = recognizer.recognize_google(audio)
    except sr.RequestError:
        outputstring = ""
    except sr.UnknownValueError:
        outputstring = ""

    return outputstring

def getweatherapi(city):
    #Get weather api from the city and format json file into a final summary list which is returned, source for api: https://openweathermap.org
    #apiurl appid = yourappid; this is my personal key, make an account on https://openweathermap.org and retrieve an api key to use in place after the "&appid="
    apiurl = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=ea198e5d7b70d11d76ac2c5e735fd8c5"
    userOutput = requests.get(apiurl.format(city))
    if userOutput:
        json = userOutput.json()
        city = json['name']
        country = json['sys']['country']
        celsius = json['main']['temp'] - 273.15
        fahrenheit = ((json['main']['temp']-273.15)*9)/5 + 32
        icon = json['weather'][0]['icon']
        description = json['weather'][0]['description']
        clothesTypes = ["Umbrella", "Raincoat", "Thick Coat", "Insulated Shoes/Gloves/Hats", "Sweaters", "Long Sleeved Shirt and Pants", "Short Sleeved Clothes"]
        # check the weather temperature range/precipitation is present and adjust the clothing label accordingly
        if fahrenheit <= 30:
            clothes = "Advised clothing: {}, {}".format(clothesTypes[2], clothesTypes[3])
        elif 30 < fahrenheit <= 40:
            clothes = "Advised clothing: {}, {}".format(clothesTypes[4], clothesTypes[5])
        elif 40 < fahrenheit <= 50:
            clothes = "Advised clothing: {}, {}".format(clothesTypes[4], clothesTypes[5])
        elif 50 < fahrenheit <= 60:
            clothes = "Advised clothing: {}".format(clothesTypes[5])
        elif 60 < fahrenheit <= 70:
            clothes = "Advised clothing: {}, {}".format(clothesTypes[5], clothesTypes[6])
        elif fahrenheit > 70:
            clothes = "Advised clothing: {}".format(clothesTypes[6])

        # check if any precipitation is in the weather description and add umbrella and raincoat if there is to advised clothing
        checkforrain = description.split()
        for word in checkforrain:
            if word.lower() == "rain":
                clothes = clothes + ", {}, {} ".format(clothesTypes[0], clothesTypes[1])
            elif word.lower() == "storm":
                clothes = clothes + ", {}, {} ".format(clothesTypes[0], clothesTypes[1])
            elif word.lower() == "snow":
                clothes = clothes + ", {}, {} ".format(clothesTypes[0], clothesTypes[1])
        summary = [city, country, celsius, fahrenheit, icon, description, clothes]
        return summary
    else:
        summary = ""
        return summary

def readybtn():
    #define the icon, reset some instructing button and label texts as the first city is being searched
    global img
    instruction['text'] = ""
    talk_btn['text'] = "Ready To Recognize Another City"
    #initialize recognizer and mic instances, then call the get speech function to get the city, which passes as a parameter into the weatherapi
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    city = getspeechinput(recognizer, microphone)
    summary = getweatherapi(city)
    #checking if summary is not empty- if it has information, update the labels accordingly, if not, then an error messagebox displays
    if summary:
        #udpate labels from api information in the summary list using indexes
        #get image from weather icons folder in the project based on the location
        img['file'] = 'weather_icons/{}.png'.format(summary[4])
        temperature['text'] = "{:.0F}°C/{:.0F}°F".format(summary[2], summary[3])
        weather['text'] = summary[5].title()
        location['text'] = '{}, {}'.format(summary[0], summary[1])
        #update time based on user time and format it in 12 hour AM/PM format with day and year
        now = datetime.now()
        time = now.strftime('%m/%d %I:%M %p')
        currenttime['text'] = "Weather As Of: {} (User Local Timezone)".format(time)
        clothes['text'] = summary[6]
    else:
        messagebox.showerror('Error', 'Speech unrecognizable or city could not be located \n Press the button and try to speak again')

#GUI display labels with weather api information provided from the weatherapi function call on button press
app = Tk()

app.title("Weather Speech Assistant")
app.geometry('600x400')
app.configure(bg='#FFFFFF')
icon = PhotoImage(file = 'weather_icons/02d.png')
app.iconphoto(False, icon)

style = Style()
style.configure('TButton', foreground = 'black', background = 'white')
style.configure('BW.TLabel', foreground = 'black', background = 'white')

location = Label(app, text="", style = 'BW.TLabel',font = ('bold', 14))
location.pack(pady = 10)

currenttime = Label(app, text = '', style = 'BW.TLabel', foreground = 'gray')
currenttime.pack(pady = 10)

temperature = Label(app, text='', font = ('bold',26), style = 'BW.TLabel')
temperature.pack()

weather = Label(app, text='', font = ('bold', 15), style = 'BW.TLabel')
weather.pack()

img = PhotoImage(file = '')
Image = Label(app, style = 'BW.TLabel', image = img)
Image.pack()

clothes = Label(app, text='', font = ('bold', 10), style = 'BW.TLabel', foreground = 'gray')
clothes.pack()

#instructions for the program, dissapear after the button is pressed once
instruction = Label(app, text = "This app will display the current weather of any city using speech recognition. \nPress the button and wait 2 seconds before saying a city for maximum clarity", font = ('bold', 12), style = 'BW.TLabel')
instruction.pack(pady = 10)

talk_btn = Button(app, text="Ready To Recognize City", style='TButton', width=28, command=readybtn, takefocus = False)
talk_btn.pack()

app.mainloop()