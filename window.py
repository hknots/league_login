from database import Database
import win32gui as win
import pyautogui as pya
import psutil
import subprocess
import os
import time

db = Database()

class Window:
    def __init__(self):
        self.name = win.GetWindowText (win.GetForegroundWindow())
        self.handle = win.FindWindow(None, self.name)
    

    @property
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @property
    def league_startup(self):
        start_attempt = True
        while start_attempt:
            time.sleep(0.1)
            if self.process_running("RiotClientServices"): # If league is running
                start_attempt = False
            else:
                try:
                    path = db.get_path # Gets default path of RiotClientServices.exe
                    start_args = [f'{path}RiotClientServices.exe', '--launch-product=league_of_legends', '--launch-patchline=live']
                    subprocess.Popen(start_args)
                    start_attempt = False
                except FileNotFoundError:
                    self.clear
                    print("RiotClientServices.exe was not found")
                    print("Paste the correct path below f.ex C:\Riot Games\Riot Client\\")
                    path = input("Path: ")
                    db.execute_commit(f"UPDATE lolpath SET path='{path}'")


    @property
    def adjust(self):
        win.MoveWindow(self.handle, 585, 315, 500, 500, False)


    def process_running(self, process_name): # Checks if proccess is running
        # Iterate over the all the running processes
        for proc in psutil.process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False;
    

    def move_top(self, window_name):
        try:
            hwnd = win.FindWindow(None, window_name)
            win.ShowWindow(hwnd,5)
            win.SetForegroundWindow(hwnd)
            rect = win.GetWindowRect(hwnd)
            time.sleep(0.2)
            return rect
        except:
            pass
    
    def look_for_login(self):
        searching = True
        count = 1
        while searching:
            time.sleep(0.1)
            picture = pya.locateOnScreen('./locate/riot.png')
            if picture:
                searching = False

            else:
                count += 1
                if count == 4:
                    count = 1

                self.clear
                print(f"Searching{count*'.'}")

                self.league_startup # Starts league if it isnt running
                self.move_top("Riot Client Main") # Move League to top

        self.move_top("Riot Client Main")
        self.move_top(self.name)


    def login(self, username, password):
        searching = True
        count = 1
        picture = pya.locateOnScreen('./locate/riot.png')
        while searching:
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
                self.move_top("Riot Client Main")
                count += 1
                if count == 4:
                    count = 1
                self.clear
                print(f"Searching{count*'.'}")
                time.sleep(0.1)