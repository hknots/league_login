import os
from database import Database
import time

db = Database()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class Menu:
    def __init__(self):
        self.options = ['Login', 'Add', 'Remove', 'Update rank', 'Exit']
    
    @property
    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def main(self):
        self.clear
        for i in range(len(self.options)):
            print("{:3^} | {}".format(i+1, self.options[i]))
    
    def add_user(self):
        user = {"username": '', "password": '', "ign": '', "server": ''}
        real_servers = ['BR1', 'EUN1', 'EUW1', 'JP1', 'LA1', 'LA2', 'NA1', 'OC1', 'TR1', 'KR', 'RU']
        servers = ['BR', 'EUN', 'EUW', 'JP', 'LA', 'NA', 'OC', 'TR', 'KR', 'RU']

        self.clear
        print("{:^3} | {}".format('0', 'Exit'))
        for key in user:
            info = input(f"{key.capitalize()}: ")

            if info == '0': # Exits
                return self.clear, print("Returning to main menu..."), time.sleep(1)

            elif key.capitalize() == 'Server': # Make sure server is a working one
                while info.upper() not in servers: # If user input is not in viable servers, ask again
                    self.clear
                    print("{:^3} | {}".format('0', 'Exit'))
                    print(f"Viable servers: {', '.join(servers)}")
                    info = input(f"{key.capitalize()}: ")
                
                if info == '0': # Exits
                    return self.clear, print("Returning to main menu..."), time.sleep(1)

                elif info.upper() == 'LA': # LA has multiple servers (1 and 2), lets user pick which one
                    self.clear
                    print("{:^3} | {}".format('0', 'Exit'))
                    print("LA got 2 servers.\nWould you like server 1 or 2?")
                    la_server = input("1 or 2: ")

                    if la_server == '0': # Exits
                        return self.clear, print("Returning to main menu..."), time.sleep(1)

                    while la_server not in ('1', '2'): # If user has not selected a valid index for LA server(1 or 2) ask again
                        self.clear
                        print("{:^3} | {}".format('0', 'Exit'))
                        print("LA got 2 servers.\nWould you like server 1 or 2?")
                        la_server = input("1 or 2: ")

                        if la_server == '0': # Exits
                            return self.clear, print("Returning to main menu..."), time.sleep(1)

                    user[key] = info.upper()+la_server# f.ex adds "LA2" to user

                elif info.upper() in [server[:-1] for server in real_servers if server[-1:] == '1']: # f.ex adds "NA1" to user
                    user[key] = info.upper()+'1'
                else:
                    user[key] = info.upper() # f.ex adds "KR" to user
            else:
                user[key] = info

        # Confirms if the user wants to add the new user to the database
        self.clear
        print(f"Are you sure you want to add {user['ign']} to the database?")
        confirm = input("Yes/No: ").capitalize()
        confirm = confirm in ("Yes", "Ye", "Y")

        if confirm: # Return user added message if True
            db.add(user['username'], user['password'], user['ign'], user['server'])
            return self.clear, print("User added!"), time.sleep(1)

        # Returns to main menu message if not True
        return self.clear, print("Returning to main menu..."), time.sleep(1)
    
    def remove_user(self):
        self.display_users()
        remove_select = input("Num: ")
        ids = db.ids

        while remove_select not in (ids + ['0']):
            self.display_users()
            remove_select = input("Num: ")

        if remove_select in ids:
            self.clear
            print("Are you sure you want to remove this user?")
            confirm = input("Yes/No: ").capitalize()
            confirm = confirm in ("Yes", 'Ye', 'Y')
            if confirm:
                db.remove(remove_select)
                return self.clear, print("User Removed!"), time.sleep(1)
            return self.clear, print("Returning to main menu..."), time.sleep(1)
    
    def display_users(self):
        self.clear
        ids = db.ids # ids in list
        igns = db.igns # Igns in list
        ranks = db.ranks # Ranks in list
        servers = db.servers # Servers in list

        column_width = db.get_column_widths # [3, 4, 6] example

        print(f"{{:^3}} | {{:^{column_width[0]}}}".format('0', 'Exit')) # Custom exit menu

        # format_string looks like {:^3} | {:^variable} | {:^variable} | {:^variable}
        format_string = f"{{:^3}} | {{:^{column_width[0]}}} | {{:^{column_width[1]}}} | {{:^{column_width[2]}}}"

        for i in range(len(igns)): # For every user, print their id, ign, rank, server
            if servers[i][-1:] in ('1', '2'): # If server ends with a number, remove it
                print(format_string.format(ids[i], igns[i], ranks[i], servers[i][:-1].upper()))
            else:
                print(format_string.format(ids[i], igns[i], ranks[i], servers[i].upper()))