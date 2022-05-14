from window import Window
from database import Database
from menu import add_menu, users_menu, main_menu, clear_terminal
from riot_api import refresh_rank

if __name__ == "__main__":
    db = Database()
    window = Window()
    window.look_for_login() # Looks for Riot login, attempts to launch and move it ontop
    window.move_ontop(window.window_name) # Moves menu on top
    
    menu = True
    while menu:
        main_menu()
        select = input("Number: ")
        while select not in ('1', '2', '3', '4', '5'):
            main_menu()
            select = input("Number: ")

        if select == '1': # Logs in
            users_menu()
            login_select = input("Num: ")
            rowids = db.rowids
            while login_select not in (rowids + ['0']):
                users_menu()
                login_select = input("Num: ")
            if login_select in rowids:
                menu = False
                login_info = db.login_info(login_select)
                window.login(login_info[0], login_info[1])
                
        elif select == '2': # Add user to database
            add_menu()

        elif select == '3': # Removes user from database
            users_menu()
            remove_select = input("Num: ")
            rowids = db.rowids
            while remove_select not in (rowids + ['0']):
                users_menu()
                remove_select = input("Num: ")
            if remove_select in rowids:
                clear_terminal()
                print("Are you sure you want to remove this user?")
                confirm = input("Yes/No: ").capitalize()
                confirm = confirm in ("Yes", 'Ye', 'Y')
                if confirm:
                    db.remove(remove_select)
                    clear_terminal()
                    print("User Removed!")
                    input("Press ANY key to continue...")

        elif select == '4': # Refresh ranks
            clear_terminal()
            print("Refreshing ranks..")
            rowids = db.rowids # example ['1', '2']
            igns = db.igns # example ['bobgamer', 'liliOTP']
            servers = db.servers # example ['euw1', 'na1']
            if len(igns) > 0:
                for i in range(len(igns)):
                    refresh_rank(rowids[i], igns[i], servers[i])
            else:
                clear_terminal()
                print("Add an user before attempting to refresh rankings")
                input("Press ANY button to continue...")

        elif select == '5': # Exits menu
            menu = False