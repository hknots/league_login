import psutil
import win32gui as win
import subprocess
import time
import pyautogui as pya
import os

from menu import clear_terminal

class Window:
    def __init__(self):
        # Stores the name of the window running the code
        self.window_name = win.GetWindowText (win.GetForegroundWindow())
        self.window = win.FindWindow(None, self.window_name)
        self.startup
        self.adjust

    @property
    def startup(self): # Starts League if it isnt running
        if not self.process_running("RiotClientServices"):
            start_args = ['C:\Riot Games\Riot Client\RiotClientServices.exe', '--launch-product=league_of_legends', '--launch-patchline=live']
            subprocess.Popen(start_args)

    @property
    def adjust(self):
        win.MoveWindow(self.window, 585, 315, 500, 500, False)
    
    @property
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def process_running(self, processName): # Checks if proccess is running
        # Iterate over the all the running processes
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if processName.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False;

    def move_ontop(self, windowName): # Moves selected window ontop
            hwnd = win.FindWindow(None, windowName)
            win.ShowWindow(hwnd,5)
            win.SetForegroundWindow(hwnd)
            rect = win.GetWindowRect(hwnd)
            return rect

    def look_for_login(self): # Looks for login logo
        searching = True
        count = 1
        while searching:
            picture = pya.locateOnScreen('./locate/riot.png')
            if picture:
                searching = False
            else:
                try:
                    self.move_ontop("Riot Client Main")
                except:
                    self.startup
                    
                count += 1
                if count == 4:
                    count = 1
                clear_terminal()
                print(f"Searching{count*'.'}")
                time.sleep(0.1)
        clear_terminal()
    
    def login(self, username, password):
        searching = True
        count = 1
        while searching:
            picture = pya.locateOnScreen('./locate/riot.png')
            if picture:
                searching = False
                cord_x = int(picture[0] + picture[2] / 2)
                cord_y = (int(picture[1] + picture[3] / 2)) + 140
                pya.click(cord_x, cord_y)
                pya.hotkey('ctrl', 'a', 'backspace')
                pya.write(username)
                cord_y = (int(picture[1] + picture[3] / 2)) + 200
                pya.click(cord_x, cord_y)
                pya.hotkey('ctrl', 'a', 'backspace')
                pya.write(password)
                pya.press('enter')
            else:
                self.move_ontop("Riot Client Main")
                count += 1
                if count == 4:
                    count = 1
                clear_terminal()
                print(f"Searching{count*'.'}")
                time.sleep(0.1)
        clear_terminal()