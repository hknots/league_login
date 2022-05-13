import os
from database import Database

db = Database()

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def add_menu():
    clear_terminal()
    username = input("Username: ")
    password = input("Password: ")
    ign = input("IGN: ")
    server = input("Server: ")
    while server not in ('euw1', 'na1'):
        clear_terminal()
        print("Available servers: euw1 or na1")
        server = input("Server: ")
    clear_terminal()
    print(f"Are you sure you want to add {ign} to the database?")
    confirmation = input("Yes/No: ").capitalize()
    confirmation = confirmation == "Yes"
    if confirmation:
        db.add(username, password, ign, server)
        clear_terminal()
        print("User added!")
        input("Press ANY button to continue...")

def main_menu():
    clear_terminal()
    menu_options = ['Login', 'Add', 'Remove', 'Refresh ranks', 'Exit']
    for i in range(len(menu_options)):
        print("{:3^} | {}".format(i+1, menu_options[i]))

def users_menu():
    clear_terminal()
    users = db.users
    rowids = db.rowids
    rowids.append('0') # Exit selection
    column_width = db.get_column_widths # [3, 4, 6] example
    format_string = f"{{:^3}} | {{:^{column_width[0]}}} | {{:^{column_width[1]}}} | {{:^{column_width[2]}}} | {{:^5}}"
    print(f"{{:^3}} | {{:^{column_width[0]}}}".format('0', 'Exit'))
    for i in range(len(users)):
        print(format_string.format(rowids[i], users[i][0], users[i][1], users[i][2], users[i][3][:-1].upper()))