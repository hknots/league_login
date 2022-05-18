from database import Database
from win32gui import GetWindowText, GetForegroundWindow, FindWindow, MoveWindow, ShowWindow, SetForegroundWindow, GetWindowRect
from pyautogui import press, locateCenterOnScreen, locateOnScreen, click, hotkey, write
from psutil import process_iter, NoSuchProcess, AccessDenied, ZombieProcess
from subprocess import Popen
from os import system, name
from time import sleep

db = Database()
login_picture = "./locate/login.png"

class Window:
    def __init__(self):
        self.name = GetWindowText (GetForegroundWindow())
        self.handle = FindWindow(None, self.name)
        self.adjust


    @property
    def clear(self):
        system('cls' if name == 'nt' else 'clear')
    

    @property
    def league_startup(self):
        start_attempt = True
        while start_attempt:
            sleep(0.1)
            if self.process_running("RiotClientServices"): # If league is running
                start_attempt = False
            else:
                try:
                    path = db.get_path # Gets default path of RiotClientServices.exe
                    start_args = [f'{path}RiotClientServices.exe', '--launch-product=league_of_legends', '--launch-patchline=live']
                    Popen(start_args)
                    start_attempt = False
                except FileNotFoundError:
                    self.clear
                    print("RiotClientServices.exe was not found")
                    print("Paste the correct path below f.ex C:\Riot Games\Riot Client\\")
                    path = input("Path: ")
                    db.execute_commit(f"UPDATE lolpath SET path='{path}'")


    @property
    def adjust(self):
        MoveWindow(self.handle, 585, 315, 650, 500, False)


    def process_running(self, process_name): # Checks if proccess is running
        # Iterate over the all the running processes
        for proc in process_iter():
            try:
                # Check if process name contains the given name string.
                if process_name.lower() in proc.name().lower():
                    return True
            except (NoSuchProcess, AccessDenied, ZombieProcess):
                pass
        return False;


    def move_top(self, window_name):
        hwnd = FindWindow(None, window_name)
        if hwnd != 0:
            ShowWindow(hwnd,5)
            press('alt')
            SetForegroundWindow(hwnd)
            rect = GetWindowRect(hwnd)
            return rect
        else:
            pass
        
    
    def look_for_login(self):
        searching = True
        while searching:
            picture = locateCenterOnScreen("./locate/login.png")
            logged_in = locateCenterOnScreen("./locate/logged_in.png")
            
            if picture:
                searching = False
            elif logged_in:
                self.clear
                print("You are logged in")
                sleep(1)
                exit()
            else:
                sleep(0.1)
                self.league_startup
                self.move_top("Riot Client Main")
    

    def login(self, username, password):
        searching = True
        while searching:
            picture = locateOnScreen("./locate/login.png")
            if picture:
                searching = False
                print(picture)
                click(int(picture[0] + picture[2] / 2), (int(picture[1] + picture[3] / 2)) + 160)
                hotkey('ctrl', 'a', 'backspace')
                write(username)

                click(int(picture[0] + picture[2] / 2), (int(picture[1] + picture[3] / 2)) + 220)
                hotkey('ctrl', 'a', 'backspace')
                write(password)
                press('enter')
            else:
                sleep(0.1)
                self.move_top("Riot Client Main")