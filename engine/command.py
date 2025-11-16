import pyttsx3
import speech_recognition as sr
import eel
import time
def speak(text):
    text = str(text)
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices') 
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 174)
    eel.DisplayMessage(text)
    engine.say(text)
    eel.receiverText(text)
    engine.runAndWait()
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.utils import speak


def takecommand():

    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening....')
        eel.DisplayMessage('listening....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source, 10, 6)
        except sr.WaitTimeoutError:
            eel.DisplayMessage('listening timed out, please try again')
            return ""

    try:
        print('recognizing')
        eel.DisplayMessage('recognizing....')
        query = r.recognize_google(audio, language='en-IN')
        print(f"user said: {query}")
        eel.DisplayMessage(query)
        time.sleep(2)
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        return ""
    except Exception as e:
        return ""
    
    return query.lower()

@eel.expose
def allCommands(message=1):
    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    
    # Guard: if recognition failed or timed out
    if not query or query.strip() == "":
        eel.DisplayMessage('I did not catch that. Please try again.')
        eel.ShowHood()
        return
    
    try:
        # Handle any YouTube intents before generic "open"
        if ("youtube" in query) or ("on youtube" in query):
            from engine.features import PlayYoutube
            PlayYoutube(query)
        elif "open" in query:
            from engine.features import openCommand
            openCommand(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp
            message = ""
            contact_no, name = findContact(query)
            if(contact_no != 0):

                #speak("Which mode you want to use whatsapp or mobile")
                #preferance = takecommand()
                #print(preferance)

                #if "mobile" in preferance:
                    #if "send message" in query or "send sms" in query: 
                        #speak("what message to send")
                        #message = takecommand()
                        #sendMessage(message, contact_no, name)
                    #elif "phone call" in query:
                        #makeCall(name, contact_no)
                    #else:
                        #speak("please try again")
                #elif "whatsapp" in preferance:
                    #message = ""
                    if "send message" in query or "send sms" in query or "message" in query:
                        message = 'message'
                        speak("what message to send")
                        message_content = takecommand()
                        if not message_content or message_content.strip() == "":
                            speak("I did not catch the message. Please try again.")
                            eel.ShowHood()
                            return
                                        
                    elif "phone call" in query or "call" in query:
                        message = 'call'
                        message_content = ""
                    else:
                        message = 'video call'
                        message_content = ""
                                        
                    whatsApp(contact_no, message_content, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)
    except Exception as e:
        print("error", e)

    
    eel.ShowHood()






# import pyttsx3
# import speech_recognition as sr
# import eel
# import time
# from engine.features import openCommand, PlayYoutube, findContact, whatsApp, makeCall, sendMessage, chatBot


# def speak(text):
#     text = str(text)
#     engine = pyttsx3.init('sapi5')
#     voices = engine.getProperty('voices')
#     engine.setProperty('voice', voices[1].id)
#     engine.setProperty('rate', 174)
#     eel.DisplayMessage(text)
#     engine.say(text)
#     eel.receiverText(text)
#     engine.runAndWait()


# def takecommand():
#     r = sr.Recognizer()
#     with sr.Microphone() as source:
#         print('listening....')
#         eel.DisplayMessage('listening....')
#         r.pause_threshold = 1
#         r.adjust_for_ambient_noise(source)
#         audio = r.listen(source, 10, 6)

#     try:
#         print('recognizing')
#         eel.DisplayMessage('recognizing....')
#         query = r.recognize_google(audio, language='en-in' or 'hindi-in')
#         print(f"user said: {query}")
#         eel.DisplayMessage(query)
#         time.sleep(2)

#     except Exception as e:
#         return ""

#     return query.lower()


# @eel.expose
# def allCommands(message=1):
#     if message == 1:
#         query = takecommand()
#         print(query)
#         eel.senderText(query)
#     else:
#         query = message
#         eel.senderText(query)

#     try:
#         if "open" in query:
#             openCommand(query)

#         elif "on youtube" in query:
#             PlayYoutube(query)

#         elif "send message" in query or "phone call" in query or "video call" in query:
#             contact_no, name = findContact(query)
#             if (contact_no != 0):
#                 speak("Which mode you want to use, WhatsApp or Mobile?")
#                 preferance = takecommand()
#                 print(preferance)

#                 if "mobile" in preferance:
#                     if "send message" in query or "send sms" in query:
#                         speak("what message to send")
#                         message = takecommand()
#                         sendMessage(message, contact_no, name)
#                     elif "phone call" in query:
#                         makeCall(name, contact_no)
#                     else:
#                         speak("please try again")

#                 elif "whatsapp" in preferance:
#                     flag = ""
#                     msg = ""
#                     if "send message" in query:
#                         flag = 'message'
#                         speak("what message to send")
#                         msg = takecommand()
#                     elif "phone call" in query:
#                         flag = 'call'
#                     else:
#                         flag = 'video'

#                     whatsApp(contact_no, msg, flag, name)

#         else:
#             chatBot(query)

#     except Exception as e:
#         print("error:", e)

#     eel.ShowHood()
