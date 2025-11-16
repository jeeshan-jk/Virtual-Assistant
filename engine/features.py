import os
import json
from shlex import quote
import re
import sqlite3
import struct
import subprocess
import time
import webbrowser
from playsound import playsound
import eel
import pyaudio
import pyautogui
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.utils import speak
from engine.config import ASSISTANT_NAME
# Playing assiatnt sound function
import pywhatkit as kit
import pvporcupine

from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

@eel.expose
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

    
def openCommand(query):
    print(f"DEBUG: openCommand called with: '{query}'")
    # Normalize first, then remove assistant name and keyword
    query = query.lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "")
    # Collapse multiple spaces
    query = re.sub(r"\s+", " ", query)

    app_name = query.strip()
    app_name_lower = app_name.lower()
    print(f"DEBUG: Processed app_name: '{app_name_lower}'")

    if app_name != "":
        # First, check for common system applications directly
        system_apps = {
            'word': [
                r"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\WINWORD.exe",
                r"C:\\Program Files\\Microsoft Office\\Office16\\WINWORD.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\Office16\\WINWORD.exe",
                r"C:\\Program Files\\Microsoft Office\\root\\Office15\\WINWORD.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office15\\WINWORD.exe",
            ],
            'excel': [
                r"C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\EXCEL.exe",
                r"C:\\Program Files\\Microsoft Office\\Office16\\EXCEL.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\Office16\\EXCEL.exe",
                r"C:\\Program Files\\Microsoft Office\\root\\Office15\\EXCEL.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office15\\EXCEL.exe",
            ],
            'powerpoint': [
                r"C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\POWERPNT.exe",
                r"C:\\Program Files\\Microsoft Office\\Office16\\POWERPNT.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\Office16\\POWERPNT.exe",
                r"C:\\Program Files\\Microsoft Office\\root\\Office15\\POWERPNT.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office15\\POWERPNT.exe",
            ],
            'outlook': [
                r"C:\\Program Files\\Microsoft Office\\root\\Office16\\OUTLOOK.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\root\\Office16\\OUTLOOK.exe",
                r"C:\\Program Files\\Microsoft Office\\Office16\\OUTLOOK.exe",
                r"C:\\Program Files (x86)\\Microsoft Office\\Office16\\OUTLOOK.exe",
            ],
            'notepad': [r"C:\\Windows\\System32\\notepad.exe"],
            'calculator': [r"C:\\Windows\\System32\\calc.exe"],
            'paint': [r"C:\\Windows\\System32\\mspaint.exe"],
            'task manager': [r"C:\\Windows\\System32\\Taskmgr.exe"],
            'control panel': [r"C:\\Windows\\System32\\control.exe"],
            'chrome': [
                r"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            ],
            'firefox': [
                r"C:\\Program Files\\Mozilla Firefox\\firefox.exe",
                r"C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe",
            ],
            'edge': [
                r"C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
                r"C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            ],
            'settings': [
                r"C:\\Windows\\System32\\ms-settings:",
                r"C:\\Windows\\System32\\control.exe",
            ],
            'calendar': [
                r"C:\\Program Files\\Windows Calendar\\wincal.exe",
                r"C:\\Windows\\System32\\outlook.exe",
            ],
            'mail': [
                r"C:\\Program Files\\Windows Mail\\winmail.exe",
                r"C:\\Windows\\System32\\outlook.exe",
            ],
            'photos': [
                r"C:\\Program Files\\Windows Photo Viewer\\PhotoViewer.exe",
                r"C:\\Program Files\\WindowsApps\\Microsoft.Windows.Photos_8wekyb3d8bbwe\\PhotosApp.exe",
            ],
            'music': [
                r"C:\\Program Files\\Windows Media Player\\wmplayer.exe",
                r"C:\\Program Files\\WindowsApps\\Microsoft.ZuneMusic_8wekyb3d8bbwe\\Music.exe",
            ],
            'video': [
                r"C:\\Program Files\\Windows Media Player\\wmplayer.exe",
                r"C:\\Program Files\\WindowsApps\\Microsoft.ZuneVideo_8wekyb3d8bbwe\\Video.exe",
            ],
            'store': [
                r"C:\\Program Files\\WindowsApps\\Microsoft.WindowsStore_8wekyb3d8bbwe\\WinStore.App.exe",
            ],
            'camera': [
                r"C:\\Program Files\\WindowsApps\\Microsoft.WindowsCamera_8wekyb3d8bbwe\\WindowsCamera.exe",
            ],
            'weather': [
                r"C:\\Program Files\\WindowsApps\\Microsoft.BingWeather_8wekyb3d8bbwe\\Weather.exe",
            ],
            'tool': [
                r"C:\\Windows\\System32\\control.exe",
            ],
            'tools': [
                r"C:\\Windows\\System32\\control.exe",
            ],
            'windows tool': [
                r"C:\\Windows\\System32\\control.exe",
            ],
            'windows tools': [
                r"C:\\Windows\\System32\\control.exe",
            ]
        }

        # Add support for WhatsApp Desktop (typical installer path)
        system_apps['whatsapp'] = [
            r"%LOCALAPPDATA%\\WhatsApp\\WhatsApp.exe",
            r"%LOCALAPPDATA%\\Programs\\WhatsApp\\WhatsApp.exe",
        ]

        # Check if it's a known system application
        print(f"DEBUG: Checking system apps for: '{app_name_lower}'")
        for app_key, paths in system_apps.items():
            if app_key in app_name_lower or app_name_lower in app_key:
                print(f"DEBUG: Found match with app_key: '{app_key}'")
                for path in paths:
                    expanded_path = os.path.expandvars(path)
                    print(f"DEBUG: Checking path: {expanded_path}")
                    # Special handling for Windows Settings
                    if app_key == 'settings' and 'ms-settings:' in path:
                        speak(f"Opening {app_name}")
                        try:
                            os.system('start ms-settings:')
                            return
                        except Exception as e:
                            print(f"Error opening settings: {e}")
                            continue
                    
                    # Check if path exists for regular applications
                    if os.path.exists(expanded_path):
                        print(f"DEBUG: Path exists, opening: {expanded_path}")
                        speak(f"Opening {app_name}")
                        try:
                            os.startfile(expanded_path)
                            return
                        except Exception as e:
                            print(f"Error opening {expanded_path}: {e}")
                            continue
                    else:
                        print(f"DEBUG: Path does not exist: {expanded_path}")
                
                # Special system commands for Windows apps
                if app_key == 'settings':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start ms-settings:')
                        return
                    except:
                        try:
                            os.system('start control')
                            return
                        except:
                            pass
                elif app_key == 'calendar':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start outlookcal:')
                        return
                    except:
                        try:
                            os.system('start calendar')
                            return
                        except:
                            pass
                elif app_key == 'mail':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start mailto:')
                        return
                    except:
                        pass
                elif app_key == 'store':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start ms-windows-store:')
                        return
                    except:
                        pass
                elif app_key == 'camera':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start microsoft.windows.camera:')
                        return
                    except:
                        pass
                elif app_key == 'weather':
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start ms-weather:')
                        return
                    except:
                        pass
                elif app_key in ['tool', 'tools', 'windows tool', 'windows tools']:
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start control')
                        return
                    except:
                        pass
                elif app_key == 'whatsapp':
                    # Try protocol handler for WhatsApp UWP/Desktop
                    try:
                        speak(f"Opening {app_name}")
                        os.system('start "" "whatsapp:"')
                        return
                    except:
                        pass
                
                # If no special handling, try generic system command
                print(f"DEBUG: No paths found, trying system command for: {app_key}")
                try:
                    speak(f"Opening {app_name}")
                    # Try different approaches based on the app
                    if app_key == 'paint':
                        os.system('start mspaint')
                    elif app_key == 'calculator':
                        os.system('start calc')
                    elif app_key == 'notepad':
                        os.system('start notepad')
                    elif app_key == 'task manager':
                        os.system('start taskmgr')
                    elif app_key == 'weather':
                        os.system('start ms-weather:')
                    elif app_key in ['tool', 'tools', 'windows tool', 'windows tools']:
                        os.system('start control')
                    else:
                        if app_key == 'whatsapp':
                            os.system('start "" "whatsapp:"')
                        else:
                            os.system(f'start {app_key}')
                    return
                except Exception as e:
                    print(f"DEBUG: System command failed: {e}")
                    pass

        try:
            # Try exact, case-insensitive match in sys_command
            cursor.execute(
                'SELECT path FROM sys_command WHERE LOWER(name) = ?', (app_name_lower,))
            results = cursor.fetchall()

            if len(results) != 0:
                db_path = results[0][0]
                print(f"DEBUG: Found in database: {db_path}")
                # Check if it's a protocol-based path (like ms-settings:)
                if ':' in db_path and not os.path.exists(db_path):
                    speak("Opening "+query)
                    try:
                        os.system(f'start {db_path}')
                        return
                    except Exception as e:
                        print(f"Error opening protocol {db_path}: {e}")
                elif os.path.exists(db_path):
                    speak("Opening "+query)
                    os.startfile(db_path)
                    return
                else:
                    # Try system command as fallback
                    try:
                        speak(f"Opening {app_name}")
                        if app_name_lower == 'whatsapp':
                            os.system('start "" "whatsapp:"')
                        else:
                            os.system(f'start {app_name_lower}')
                        return
                    except:
                        pass

            # Try exact, case-insensitive match in web_command
            cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name) = ?', (app_name_lower,))
            results = cursor.fetchall()
            
            if len(results) != 0:
                speak("Opening "+query)
                webbrowser.open(results[0][0])
                return

            # Try partial match in web_command
            cursor.execute(
                'SELECT url FROM web_command WHERE LOWER(name) LIKE ?', ('%'+app_name_lower+'%',))
            results = cursor.fetchall()
            if len(results) != 0:
                speak("Opening "+query)
                webbrowser.open(results[0][0])
                return
            
            # Try system command as last resort
            try:
                speak(f"Opening {app_name}")
                if app_name_lower == 'whatsapp':
                    os.system('start "" "whatsapp:"')
                else:
                    os.system(f'start {app_name_lower}')
                return
            except:
                pass
            
            # Only search web if it looks like a website
            if re.search(r"\.[a-z]{2,}$", app_name_lower) or any(web_indicator in app_name_lower for web_indicator in ['website', 'site', 'web', 'online', 'search']):
                speak("Searching web for "+app_name_lower)
                webbrowser.open("https://www.google.com/search?q="+app_name_lower)
            else:
                speak(f"Could not find '{app_name_lower}'. Please check the application name or install the application.")
                
        except Exception as e:
            print(f"Error in openCommand: {e}")
            speak("Something went wrong")

       

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term and search_term.strip() != "":
        speak("Playing "+search_term+" on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com/")


def hotword():
    porcupine=None
    paud=None
    audio_stream=None
    try:
        print("Starting hotword detection...")
        # pre trained keywords    
        porcupine=pvporcupine.create(keywords=["jarvis","alexa"]) 
        paud=pyaudio.PyAudio()
        audio_stream=paud.open(rate=porcupine.sample_rate,channels=1,format=pyaudio.paInt16,input=True,frames_per_buffer=porcupine.frame_length)
        
        print("Hotword detection active. Say 'Jarvis' or 'Alexa' to activate.")
        
        # loop for streaming
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            # processing keyword comes from mic 
            keyword_index=porcupine.process(keyword)

            # checking first keyword detected for not
            if keyword_index>=0:
                print("hotword detected")
                
                # Use Win+J shortcut to activate Windows Voice Typing
                # This is more reliable than trying to call eel functions from another process
                try:
                    import pyautogui as autogui
                    autogui.keyDown("win")
                    autogui.press("j")
                    time.sleep(0.1)
                    autogui.keyUp("win")
                    print("Voice activation triggered via Win+J")
                except Exception as e:
                    print(f"Voice activation failed: {e}")
                    # Alternative: try Ctrl+Shift+S or other voice shortcuts
                    try:
                        autogui.hotkey("ctrl", "shift", "s")
                        print("Alternative voice activation triggered")
                    except Exception as alt_error:
                        print(f"Alternative activation also failed: {alt_error}")
                
    except Exception as e:
        print(f"Hotword detection error: {e}")
    finally:
        # Proper cleanup
        if porcupine is not None:
            try:
                porcupine.delete()
            except:
                pass
        if audio_stream is not None:
            try:
                audio_stream.close()
            except:
                pass
        if paud is not None:
            try:
                paud.terminate()
            except:
                pass
        print("Hotword detection stopped.")



# find contacts
def findContact(query):
    
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
        results = cursor.fetchall()
        print(results[0][0])
        mobile_number_str = str(results[0][0])

        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str

        return mobile_number_str, query
    except:
        speak('not exist in contacts')
        return 0, 0
    
def whatsApp(mobile_no, message, flag, name):
    

    if flag == 'message':
        target_tab = 20
        jarvis_message = "message send successfully to "+name

    elif flag == 'call':
        target_tab = 14
        message = ''
        jarvis_message = "calling to "+name

    else:
        target_tab = 12
        message = ''
        jarvis_message = "staring video call with "+name


    # Encode the message for URL
    encoded_message = quote(message)
    #print(encoded_message)
    # Construct the URL
    whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    # Construct the full command
    full_command = f'start "" "{whatsapp_url}"'

    # Open WhatsApp with the constructed URL using cmd.exe
    subprocess.run(full_command, shell=True)
    time.sleep(5)
    subprocess.run(full_command, shell=True)
    
    pyautogui.hotkey('ctrl', 'f')

    for i in range(1, target_tab):
        pyautogui.hotkey('tab')

    pyautogui.hotkey('enter')
    speak(jarvis_message)

# chat bot
# Initialize holder; will create ChatBot lazily inside chatBot to avoid init-time failures
# #_hugging_chatbot = None

def chatBot(query):
    user_input = query.lower()
    chatbot = hugchat.ChatBot(cookie_path=r"engine\cookies.json")
    id = chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response
    


def makeCall(name, mobileNo):
    mobileNo =mobileNo.replace(" ", "")
    speak("Calling "+name)
    command = 'adb shell am start -a android.intent.action.CALL -d tel:'+mobileNo
    os.system(command)


# to send message
def sendMessage(message, mobileNo, name):
    from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
    message = replace_spaces_with_percent_s(message)
    mobileNo = replace_spaces_with_percent_s(mobileNo)
    speak("sending message")
    goback(4)
    time.sleep(1)
    keyEvent(3)
    # open sms app
    tapEvents(136, 2220)
    #start chat
    tapEvents(819, 2192)
    # search mobile no
    adbInput(mobileNo)
    #tap on name
    tapEvents(601, 574)
    # tap on input
    tapEvents(390, 2270)
    #message
    adbInput(message)
    #send
    tapEvents(957, 1397)
    speak("message send successfully to "+name)






# import os
# import sqlite3
# import struct
# import subprocess
# import time
# import webbrowser
# import urllib.parse
# import pyautogui
# import pyaudio
# import pvporcupine
# import pywhatkit as kit
# from shlex import quote
# from playsound import playsound
# import eel
# from engine.utils import speak
# from engine.config import ASSISTANT_NAME
# from engine.helper import extract_yt_term, remove_words
# import hugchat


# con = sqlite3.connect("jarvis.db")
# cursor = con.cursor()


# @eel.expose
# def playAssistantSound():
#     music_dir = "www\\assets\\audio\\start_sound.mp3"
#     playsound(music_dir)


# def openCommand(query):
#     query = query.replace(ASSISTANT_NAME, "")
#     query = query.replace("open", "")
#     query.lower()

#     app_name = query.strip()

#     if app_name != "":
#         try:
#             cursor.execute(
#                 'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
#             results = cursor.fetchall()

#             if len(results) != 0:
#                 speak("Opening " + query)
#                 os.startfile(results[0][0])

#             elif len(results) == 0:
#                 cursor.execute(
#                     'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
#                 results = cursor.fetchall()

#                 if len(results) != 0:
#                     speak("Opening " + query)
#                     webbrowser.open(results[0][0])

#                 else:
#                     speak("Opening " + query)
#                     try:
#                         os.system('start ' + query)
#                     except:
#                         speak("not found")
#         except:
#             speak("something went wrong")


# def PlayYoutube(query):
#     search_term = extract_yt_term(query)
#     speak("Playing " + search_term + " on YouTube")
#     kit.playonyt(search_term)


# def hotword():
#     porcupine = None
#     paud = None
#     audio_stream = None
#     try:
#         porcupine = pvporcupine.create(keywords=["jarvis", "alexa"])
#         paud = pyaudio.PyAudio()
#         audio_stream = paud.open(
#             rate=porcupine.sample_rate,
#             channels=1,
#             format=pyaudio.paInt16,
#             input=True,
#             frames_per_buffer=porcupine.frame_length
#         )

#         while True:
#             keyword = audio_stream.read(porcupine.frame_length)
#             keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)
#             keyword_index = porcupine.process(keyword)

#             if keyword_index >= 0:
#                 print("hotword detected")
#                 import pyautogui as autogui
#                 autogui.keyDown("win")
#                 autogui.press("j")
#                 time.sleep(2)
#                 autogui.keyUp("win")

#     except:
#         if porcupine is not None:
#             porcupine.delete()
#         if audio_stream is not None:
#             audio_stream.close()
#         if paud is not None:
#             paud.terminate()


# # find contacts
# def findContact(query):
#     words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'phone',
#                        'call', 'send', 'message', 'whatsapp', 'video']
#     query = remove_words(query, words_to_remove)

#     try:
#         query = query.strip().lower()
#         cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
#                        ('%' + query + '%', query + '%'))
#         results = cursor.fetchall()
#         print(results[0][0])
#         mobile_number_str = str(results[0][0])

#         if not mobile_number_str.startswith('+91'):
#             mobile_number_str = '+91' + mobile_number_str

#         return mobile_number_str, query
#     except:
#         speak('not exist in contacts')
#         return 0, 0


# # ✅ Fixed WhatsApp integration
# def whatsApp(mobile_no, message, flag, name):
#     if flag == 'message':
#         jarvis_message = "Message sent successfully to " + name
#     elif flag == 'call':
#         message = ''
#         jarvis_message = "Calling " + name
#     else:
#         message = ''
#         jarvis_message = "Starting video call with " + name

#     # Encode safely
#     encoded_message = urllib.parse.quote(message)

#     # WhatsApp deep link
#     whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

#     # Open WhatsApp Desktop
#     os.system(f'start "" "{whatsapp_url}"')
#     time.sleep(5)

#     # Action
#     if flag == 'message':
#         pyautogui.press("enter")
#     elif flag == 'call':
#         pyautogui.hotkey("ctrl", "shift", "c")
#     else:
#         pyautogui.hotkey("ctrl", "shift", "v")

#     speak(jarvis_message)


# # chat bot
# def chatBot(query):
#     user_input = query.lower()
#     chatbot = hugchat.ChatBot(cookie_path="engine\cookies.json")
#     id = chatbot.new_conversation()
#     chatbot.change_conversation(id)
#     response = chatbot.chat(user_input)
#     print(response)
#     speak(response)
#     return response


# # android automation
# def makeCall(name, mobileNo):
#     mobileNo = mobileNo.replace(" ", "")
#     speak("Calling " + name)
#     command = 'adb shell am start -a android.intent.action.CALL -d tel:' + mobileNo
#     os.system(command)


# def sendMessage(message, mobileNo, name):
#     from engine.helper import replace_spaces_with_percent_s, goback, keyEvent, tapEvents, adbInput
#     message = replace_spaces_with_percent_s(message)
#     mobileNo = replace_spaces_with_percent_s(mobileNo)
#     speak("sending message")
#     goback(4)
#     time.sleep(1)
#     keyEvent(3)
#     tapEvents(136, 2220)
#     tapEvents(819, 2192)
#     adbInput(mobileNo)
#     tapEvents(601, 574)
#     tapEvents(390, 2270)
#     adbInput(message)
#     tapEvents(957, 1397)
#     speak("message sent successfully to " + name)
