import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import pyaudio
from playsound import playsound
import random
import webbrowser
import wolframalpha


'''ignore any warnings'''
warnings.filterwarnings('ignore')

'''wolframalpha'''
APP_ID = ''


def assistanceResponse(text) :
    '''convert text to speach'''
    output = gTTS(text=text, lang='en', slow=False)
    '''save the file'''
    output.save('response.mp3')
    '''play the converted file'''
    playsound('response.mp3')
    os.remove('response.mp3')

'''record audio and return text'''
def recordAudio(ask = False) :
    '''record the audio'''
    #r = sr.Recognizer()
    '''creating a recognizer object'''
    '''open mic and start recording'''
    r.adjust_for_ambient_noise(source, duration=0.5)
    if ask :
        assistanceResponse(ask)
    else:
        assistanceResponse('how can I help you?')
    print('Listening...')
    audio = r.listen(source,phrase_time_limit= 5)
    '''use googles speech rocognition'''
    input_text = ''
    try :
        input_text = r.recognize_google(audio)
        print('You said : ' + input_text)
    except sr.UnknownValueError :
        '''Check for unknown errors'''
        print('Google speech recognition could not understand your audio, unknown error.')
        assistanceResponse('sorry, I did not get that.')
    except sr.RequestError as e :
        print('Request results from google speech recognition error : ' + e)
        assistanceResponse('sorry, my services seems to be down at the moment.')
    return input_text.lower()


class assistFunctions :
    '''Functions of the AI'''

    def __init__(self,AudioText):
        self.AudioText = AudioText

    def nameCheck(self) :
        responses = ['What do you care?','My name is Eera']
        rand = random.randint(0,len(responses)-1)
        assistanceResponse(responses[rand])

    def showDate(self) :
        x = datetime.datetime.now()
        print(x.strftime("%A, %m/%d/%y"))
        response = x.strftime("%A %d %B %Y")
        assistanceResponse("Today is " + response)

    def showTime(self) :
        current_time = datetime.datetime.now().strftime("%H:%M")
        current_time = current_time.split(':')
        if int(current_time[0]) < 12 :
            current_time = f'{current_time[0]}:{current_time[1]} AM'
        elif int(current_time[0]) == 12 :
            current_time = f'{current_time[0]}:{current_time[1]} PM'
        else :
            current_time = f'{int(current_time[0])-12}:{current_time[1]} PM'
        print(current_time)
        assistanceResponse('It is currently ' + current_time)

    def search(self) :
        search = recordAudio('what would you like to search for?')
        url = 'https://google.com/search?q=' + search
        webbrowser.open_new_tab(url)
        assistanceResponse('showing results for ' + search)

    def playYoutube(self) :
        search = recordAudio('what would you like to play on youtube?')
        url = 'https://www.youtube.com/results?search_query=' + search
        webbrowser.open_new_tab(url)
        assistanceResponse('showing results for ' + search)

    def makeNote(self) :
        text = recordAudio('What should I write?')
        now = datetime.datetime.now()
        currentDate = str(now.month) + "-" + str(now.day) + "_" + str(now.hour) + "-" + str(now.minute) + "-" + str(now.second)
        file_path = 'note-{}.txt'.format(currentDate)
        file = open(file_path, 'w')
        file.write(text)
        file.close()
        assistanceResponse("Noted. Here it is.")
        os.system(file_path)

    def wolf(self) :
        client = wolframalpha.Client(APP_ID)
        res = client.query(self.AudioText)
        answer = next(res.results).text
        print(answer)
        assistanceResponse(answer)

    def runFunction(self) :
        if 'your name' in self.AudioText :
            self.nameCheck()
            return
            '''
        for phrase in ["what's the time", 'what time is it','tell me the time','give me the time'] :
            if phrase in self.AudioText :
                self.showTime()
                return
                '''
        for phrase in ["what's the date", 'what day is it', 'tell me the date',"today's date"]:
            if phrase in self.AudioText:
                self.showDate()
                return
        if 'search' in self.AudioText :
            self.search()
            return
        for phrase in ['play on youtube','open in youtube','search on youtube'] :
            if phrase in self.AudioText :
                self.playYoutube()
                return
        for phrase in ['make note of','take a note','make a note'] :
            if phrase in self.AudioText :
                self.makeNote()
                return
        self.wolf()


currentPath = os.path.abspath(__file__).rstrip('virtual_assistant.py')


'''MAIN'''
assistanceResponse('Starting up.')
playsound(currentPath + 'PowerUp - Sound Effects.mp3')
assistanceResponse('System online.')
r = sr.Recognizer()
with sr.Microphone() as source:
    r.pause_threshold = 0.5
    r.adjust_for_ambient_noise(source)
    while True :
        print('Listening...')
        audio = r.listen(source,timeout=None, phrase_time_limit=3)
        try:
            wake_text = r.recognize_google(audio)
            print(wake_text)
        except:
            print('exception')
            continue

        if 'hey' in wake_text:
            textAudio = recordAudio()
            main = assistFunctions(textAudio)
            main.runFunction()

        if 'exit' in wake_text :
            assistanceResponse('Shutting down.')
            playsound(currentPath + 'Shut-down-sound-effect.mp3')
            break
        print('next loop')

print('end')
