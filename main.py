#CoronaVirus Cases Website-https://www.worldometers.info/coronavirus/
#API Key-t2dq1i4Eag2W
#Project Token-tDtxymiHvO1p
#Run Token-tMarsGesyo4k


import requests
import json
import pyttsx3
import speech_recognition as sr
import re

API_KEY= "t2dq1i4Eag2W"
PROJECT_TOKEN= "tDtxymiHvO1p"
RUN_TOKEN= "t8JvBmPjTd7P"


class Data:

    def __init__(self, api_key, project_token):
        self.api_key = api_key
        self.project_token = project_token
        self.params = {
            "api_key" : self.api_key
        }
        self.data = self.get_data()


    #Call the request and get the whole data
    def get_data(self):
        response = requests.get(f'https://www.parsehub.com/api/v2/projects/{self.project_token}/last_ready_run/data',params=self.params)
        data=json.loads(response.text)
        return data


    #Retuning the total cases
    def get_total_cases(self):
        data = self.data['total']

        for val in data:
            if val['name'] == 'Coronavirus Cases:':
                return val['values']
        return 'N/A'

    def get_total_deaths(self):
        data = self.data['total']
        for val in data:
            if val['name'] == 'Deaths:':
                return val['values']
        return 'N/A'

    def get_total_recovered(self):
        data = self.data['total']

        for val in data:
            if val['name'] == 'Recovered:':
                return val['values']
        return 'N/A'


    #Get Searched Country data
    def get_country_data(self,search_country):
        countrylist = self.data['country']
        for con in countrylist:
            if con['name'].lower()==search_country.lower():
                return con
        return 'N/A'

    def get_list_of_countries(self):
        countries=[]
        data = self.data['country']
        for con in data:
            countries.append(con['name'].lower())
        return countries


def speak(text):
    engine=pyttsx3.init()                    #It initialize the engine
    engine.say(text)                         #It will speak
    engine.runAndWait()                      #Speak And Wait


def get_audio():
    r=sr.Recognizer()                       #Setup the Recognizer
    with sr.Microphone() as source:         #Listen
        audio = r.listen(source)            #Record it
        said = ""

        try:
            said=r.recognize_google(audio)  #Convert the record audio to string
        except Exception as e:
            print("Exception as ",str(e))
    return said.lower()


def main():
    print("Program Started")
    speak("Welcome Diptiman")
    print("Welcome Diptiman")

    data=Data(API_KEY,PROJECT_TOKEN)
    END_PHRASE="stop"
    country_list=data.get_list_of_countries()


    TOTAL_PATTERN = {
                    re.compile("[\w\s]+ total [\w\s]+ cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total cases"):data.get_total_cases,
                    re.compile("[\w\s]+ total [\w\s]+ deaths"):data.get_total_deaths,
                    re.compile("[\w\s]+ total [\w\s]+ death"): data.get_total_deaths,
                    re.compile("[\w\s]+ total deaths"):data.get_total_deaths
    }

    COUNTRY_PATTERN = {
                    re.compile("[\w\s]+ total recovered [\w\s]+"): lambda country: data.get_country_data(country)['active_cases'],
                    re.compile("[\w\s]+ active cases [\w\s]+"): lambda country: data.get_country_data(country)['active_cases'],
                    re.compile("[\w\s]+ cases [\w\s]+"):lambda country:data.get_country_data(country)['total_cases'],
                    re.compile("[\w\s]+ deaths [\w\s]+"): lambda country: data.get_country_data(country)['total_deaths'],
    }

    while True:
        print("Listening")
        text=get_audio()
        print(text)
        result=None

        for pattern,func in COUNTRY_PATTERN.items():
            if pattern.match(text):
                words=set(text.split(" "))
                for country in country_list:
                    if country in words:
                        result=func(country)
                        break


        for pattern,func in TOTAL_PATTERN.items():
            if pattern.match(text):
                result=func()
                break;

        if result:
            speak(text+" is ")
            speak(result)
            print(result)
        else:
            speak(text)

        if END_PHRASE in text:  # stop loop
            print("Bye Bye!")
            speak("Have A Good Day!")
            break
        print("\n")

main()