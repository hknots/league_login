import os
from database import Database
import time

db = Database()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_menu():
    clear_terminal()
    username = input("Username: ")
    password = input("Password: ")
    ign = input("IGN: ")
    server = input("Server: ")

    while server not in ('euw1', 'na1'): # If server not valid
        clear_terminal()
        print("Available servers: euw1 or na1")
        server = input("Server: ")

    clear_terminal()
    print(f"Are you sure you want to add {ign} to the database?")
    confirmation = input("Yes/No: ").capitalize()
    confirmation = confirmation in ("Yes", "Ye", "Y")
    if confirmation: # Checks if user wants to add user to terminal
        db.add(username, password, ign, server)
        clear_terminal()
        print("User added!")
        time.sleep(1)

def main_menu():
    clear_terminal()
    menu_options = ['Login', 'Add', 'Remove', 'Refresh ranks', 'Exit']
    for i in range(len(menu_options)):
        print("{:3^} | {}".format(i+1, menu_options[i]))

def users_menu():
    clear_terminal()
    rowids = db.rowids # Rows in database as strings f.ex ['1', '2', '3']
    igns = db.igns
    ranks = db.ranks
    servers = db.servers
    rowids.append('0') # Exit selection
    column_width = db.get_column_widths # [3, 4, 6] example

    print(f"{{:^3}} | {{:^{column_width[0]}}}".format('0', 'Exit')) # Custom exit menu

    format_string = f"{{:^3}} | {{:^{column_width[0]}}} | {{:^{column_width[1]}}} | {{:^{column_width[2]}}}" # placeholders looks like {:^variable}
    for i in range(len(igns)): # For every user, print their rowid, ign, rank, server
        print(format_string.format(rowids[i], igns[i], ranks[i], servers[i][:-1].upper()))