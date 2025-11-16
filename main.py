import os
import eel
import subprocess
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.features import *
from engine.command import *
from engine.utils import speak
from engine.auth import recoganize
def start():
    
    eel.init("www")

    playAssistantSound()
    @eel.expose
    def init():
        try:
            # Check if ADB is available
            result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
            if result.returncode == 0:
                subprocess.call([r'device.bat'])
            else:
                print("ADB not available, skipping device connection")
        except FileNotFoundError:
            print("ADB not found in PATH, skipping device connection")
        except Exception as e:
            print(f"ADB check error: {e}")
        
        eel.hideLoader()
        speak("Ready for Face Authentication")
        
        try:
            flag = recoganize.AuthenticateFace()
            if flag == 1:
                eel.hideFaceAuth()
                speak("Face Authentication Successful")
                eel.hideFaceAuthSuccess()
                speak("Hello, Welcome Sir, How can i Help You")
                eel.hideStart()
                playAssistantSound()
            else:
                speak("Face Authentication Failed")
                print("Face authentication failed")
        except Exception as e:
            print(f"Face authentication error: {e}")
            speak("Face Authentication Error - Please try again")
    os.system('start msedge.exe --app="http://localhost:8000/index.html"')

    eel.start('index.html', mode=None, host='localhost', block=True)