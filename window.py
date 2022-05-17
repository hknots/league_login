from database import Database
import win32gui as win
import pyautogui as pya
import psutil
import subprocess
import os
import time

db = Database()
login_picture = "./locate/login.png"

class Window:
    def __init__(self):
        self.name = win.GetWindowText (win.GetForegroundWindow())
        self.handle = win.FindWindow(None, self.name)
        self.adjust


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
        win.MoveWindow(self.handle, 585, 315, 650, 500, False)


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
        hwnd = win.FindWindow(None, window_name)
        if hwnd != 0:
            win.ShowWindow(hwnd,5)
            pya.press('alt')
            win.SetForegroundWindow(hwnd)
            rect = win.GetWindowRect(hwnd)
            return rect
        else:
            pass
        
    
    def look_for_login(self):
        searching = True
        while searching:
            picture = pya.locateCenterOnScreen("./locate/login.png")
            logged_in = pya.locateCenterOnScreen("./locate/logged_in.png")
            
            if picture:
                searching = False
            elif logged_in:
                self.clear
                print("You are logged in")
                time.sleep(1)
                exit()
            else:
                time.sleep(0.1)
                self.league_startup
                self.move_top("Riot Client Main")
    

    def login(self, username, password):
        searching = True
        while searching:
            picture = pya.locateOnScreen("./locate/login.png")
            if picture:
                searching = False
                print(picture)
                pya.click(int(picture[0] + picture[2] / 2), (int(picture[1] + picture[3] / 2)) + 160)
                pya.hotkey('ctrl', 'a', 'backspace')
                pya.write(username)

                pya.click(int(picture[0] + picture[2] / 2), (int(picture[1] + picture[3] / 2)) + 220)
                pya.hotkey('ctrl', 'a', 'backspace')
                pya.write(password)
                pya.press('enter')
            else:
                time.sleep(0.1)
                self.move_top("Riot Client Main")