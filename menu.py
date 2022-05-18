from msvcrt import getch
from database import Database
from riot_api import refresh_rank, valid_api
from window import Window
from os import system, name

window = Window()
db = Database()

class Menu:
    def __init__(self):
        self.options = ["Login", "Add user", "Remove user", "Modify user", "Update rank", "Exit"]
    
    @property
    def clear(self):
        system('cls' if name == 'nt' else 'clear')
    
    
    @property
    def select_server(self):
        digit_servers = ['BR', 'EUN', 'EUW', 'JP', 'LA', 'NA', 'OC', 'TR'] # Servers with either '1' or '2' after the name
        servers = ['KR', 'RU'] # Servers with no digits at the end

        selecting_server = True
        while selecting_server:
            self.clear
            self.exit_message(0)
            print(f"Viable servers: {', '.join(digit_servers+servers)}")
            server = input("Server: ").upper()

            if server in servers:
                return server
            elif server in digit_servers:
                if server != "LA":
                    return server + '1'

                selecting_la_server = True
                while selecting_la_server:
                    self.clear
                    self.exit_message(0)
                    print("LA has 2 servers, select 1 or 2.")
                    la_server = input("select: ")
                    
                    if la_server in ("1", "2"):
                        return server+la_server # f.ex LA2
            elif server == "0":
                return "0"
    

    def centre_message(self, msg, width):
        print(f"{{:^{width}}}".format(msg))
    

    def exit_message(self, width):
        self.centre_message("Enter 0 To Exit", width)


    def main(self):
        self.clear
        for i in range(len(self.options)):
            print("{:^3} | {}".format(i + 1, self.options[i]))
    

    def add_user(self):
        self.clear
        user = {"username": '',"password": '', "ign": '', "server": ''}
        for key in user:
            if key == "server":
                info = self.select_server # Lets user only pick real servers
            else:
                self.clear
                self.exit_message(0)
                info = input(f"{key.capitalize()}: ")
            if info == "0": # Exits to main menu
                return
            user[key] = info # Adds the information to dictionary
        db.add_user(user["username"], user["password"], user["ign"], user["server"])
        

    def display_user(self, id=0, dis_id=True, dis_username=False, dis_password=False, dis_ign=True, dis_rank=True, dis_server=True, dis_all=False, dis_column=False):
        self.clear # Clears terminal
        if id == 0:
            users = db.get_user() # Dictionary containing information about every user
        elif id in db.get_ids:
            users = db.get_user(id=id) # Dictionary containing information about every user

        if id == 0:
            col_widths = db.get_column_width() # Dictionary containing the len() of biggest item in column
        elif id in db.get_ids:
            col_widths = db.get_column_width(id=id)
            
        display_bool = {"id": dis_id, "username": dis_username, "password": dis_password, "ign": dis_ign, "rank": dis_rank, "server": dis_server}
        display = []

        if dis_all:
            for key in display_bool:
                display_bool[key] = True

        format_string = ""
        for key in display_bool: # Checks for what to print out
            if display_bool[key]: # If True, add to list and format_string
                display.append(str(key))
                if key == "id":
                    format_string += "{:^3} | "
                else:
                    format_string += f"{{:^{col_widths[key]}}} | "
        format_string = format_string[:-2] # Removes the line at the end of the string f.ex "| "

        width = len(format_string.format(*display))
        self.exit_message(width)
        
        if dis_column: # displays column name
            print(format_string.format(*[column.upper() for column in display]))
        for i in range(len(users['id'])): # For every user registered

            if users['server'][i][-1:] in ("1", "2"): # If the server has a digit
                users['server'][i] = users['server'][i][:-1] # Remove digit at the end of string
            print(format_string.format(*[users[display[x]][i] for x in range(len(display))]))


    def remove_user(self):
        removing = True
        while removing:
            self.display_user(dis_column=True)
            remove_id = input("ID: ")
            if remove_id in db.get_ids:
                db.remove(remove_id)
            elif remove_id == "0":
                removing = False
    

    def modify_user(self):
        modifying = True
        while modifying:
            self.display_user(dis_column=True)
            modify_id = input("ID: ")
            if modify_id in db.get_ids:
                modifiyng_user = True
                while modifiyng_user:
                    self.display_user(id=modify_id, dis_all=True, dis_column=True)
                    modify_column = input("Column: ").lower()

                    if modify_column in db.get_columns: # If selection is in columns
                        for column in db.get_columns: # Goes through every column name
                            if modify_column == column: # If user selection is equals to column
                                if column == "id": # If user selected id
                                    selecting_id = True
                                    while selecting_id:
                                        self.clear
                                        self.exit_message(0)
                                        viable_ids = [i for i in db.get_ids if i != modify_id] # Ids that is not the current users id
                                        print(f"Viable ids: {', '.join(viable_ids)}") # Displays all viable ids
                                        modify_change = input(f"{modify_column.capitalize()}: ")

                                        if modify_change in viable_ids:
                                            db.update_id(modify_id, modify_change)
                                            modify_id = modify_change
                                            selecting_id = False
                                        elif modify_change == "0":
                                            selecting_id = False

                                elif column == "server":
                                    modify_change = self.select_server
                                    if modify_change != "0":
                                        db.update_user(modify_column, modify_change, modify_id)

                                else: # All other columns
                                    self.clear
                                    self.exit_message(0)
                                    modify_change = input(f"{modify_column.capitalize()}: ")
                                    if modify_change != "0":
                                        db.update_user(modify_column, modify_change, modify_id)

                    elif modify_column == "0": # Return to modify menu
                        modifiyng_user = False

            elif modify_id == "0": # Return to main menu
                modifying = False


    def update_rank(self):
        self.clear
        if len(db.get_ids) < 1: # Checks if users exist
            print("No users detected!")
            print("Press ANY key to continue")
            getch() # Returns once a key is pressed

        elif not valid_api(): # Invalid API
            self.exit_message(0)
            print("Invalid API - Get your personal API from: https://developer.riotgames.com/")
            new_api = input("API: ")
            if new_api != "0":
                db.update_api(new_api)
                return self.update_rank()

        else: # If valid API
            users = db.get_user()
            x = 0
            for i in range(len(users['id'])): # For every user
                x += 1
                if x == 4:
                    x = 0
                print(f"Updating ranks{x*'.'}") # Loading dots . . .
                refresh_rank(users['id'][i])
                self.clear
    

    def login(self):
        logging_in = True
        while logging_in:
            self.clear
            self.display_user(dis_column=True)
            login = input("ID: ")
            
            if login in db.get_ids:
                user = db.get_user(id=login)
                window.login(user['username'][0], user['password'][0])
                exit() # Closes program
            elif login == "0":
                logging_in = False

